import os
import pandas as pd

from datetime import datetime

from storage.lakehouse.minio_client import client

from lineage.openlineage_emitter import (
    start_run,
    complete_run,
    fail_run,
)


def upload_batch_to_lake(
        messages,
        bucket_name,
        dataset_name
):

    if not messages:
        return

    df = pd.DataFrame(messages)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_name = f"{dataset_name}_{timestamp}.parquet"

    df.to_parquet(file_name, index=False)

    today = datetime.now()

    object_name = (
        f"{dataset_name}/"
        f"{today.year}/"
        f"{today.month:02}/"
        f"{today.day:02}/"
        f"{file_name}"
    )

    output_dataset = f"s3://{bucket_name}/{object_name}"

    run_id = start_run(
        job_name=f"{dataset_name}-pipeline",
        input_dataset=dataset_name,
        output_dataset=output_dataset,
    )

    try:

        client.fput_object(
            bucket_name,
            object_name,
            file_name
        )

        complete_run(
            run_id=run_id,
            job_name=f"{dataset_name}-pipeline",
            input_dataset=dataset_name,
            output_dataset=output_dataset,
        )

        print(f"Uploaded: {output_dataset}")

    except Exception:

        fail_run(
            run_id=run_id,
            job_name=f"{dataset_name}-pipeline",
            input_dataset=dataset_name,
            output_dataset=output_dataset,
        )

        raise

    finally:

        if os.path.exists(file_name):
            os.remove(file_name)