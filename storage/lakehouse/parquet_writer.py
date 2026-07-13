import os
from datetime import datetime

import pandas as pd

from storage.lakehouse.minio_client import client

from lineage.openlineage_emitter import (
    build_schema_facet,
    dataframe_schema_fields,
    start_run,
    complete_run,
    fail_run,
)


def upload_batch_to_lake(
    messages,
    bucket_name,
    dataset_name,
    source_name,
):
    """
    Upload a batch of Kafka messages to MinIO and emit
    OpenLineage events.

    Parameters
    ----------
    messages : list
        Batch of Kafka messages.

    bucket_name : str
        MinIO bucket name.

    dataset_name : str
        Logical dataset name
        (e.g. meter-data, command-response).

    source_name : str
        Source system name
        (Kafka topic).
    """

    if not messages:
        return

    df = pd.DataFrame(messages)
    schema_fields = dataframe_schema_fields(df)
    schema_facet = build_schema_facet(schema_fields)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_name = f"{dataset_name}_{timestamp}.parquet"

    df.to_parquet(
        file_name,
        index=False
    )

    today = datetime.now()

    object_name = (
        f"{dataset_name}/"
        f"{today.year}/"
        f"{today.month:02}/"
        f"{today.day:02}/"
        f"{file_name}"
    )

    object_path = f"s3://{bucket_name}/{object_name}"

    # ----------------------------------------------------------
    # OpenLineage START
    # ----------------------------------------------------------

    run_id = start_run(
        job_name=f"{dataset_name}-pipeline",
        input_namespace="kafka",
        input_dataset=source_name,
        output_namespace="minio",
        output_dataset=dataset_name,
        output_dataset_facets=schema_facet,
    )

    try:

        client.fput_object(
            bucket_name=bucket_name,
            object_name=object_name,
            file_path=file_name,
        )

        complete_run(
            run_id=run_id,
            job_name=f"{dataset_name}-pipeline",
            input_namespace="kafka",
            input_dataset=source_name,
            output_namespace="minio",
            output_dataset=dataset_name,
            output_dataset_facets=schema_facet,
        )

        print(f"Uploaded: {object_path}")

    except Exception:

        fail_run(
            run_id=run_id,
            job_name=f"{dataset_name}-pipeline",
            input_namespace="kafka",
            input_dataset=source_name,
            output_namespace="minio",
            output_dataset=dataset_name,
            output_dataset_facets=schema_facet,
        )

        raise

    finally:

        if os.path.exists(file_name):
            os.remove(file_name)
