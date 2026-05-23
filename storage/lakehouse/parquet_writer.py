import pandas as pd

from datetime import datetime

from storage.lakehouse.minio_client import client


def upload_batch_to_lake(
        messages,
        bucket_name,
        dataset_name
):

    if not messages:
        return

    df = pd.DataFrame(messages)

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

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

    client.fput_object(
        bucket_name,
        object_name,
        file_name
    )

    print(f"Uploaded: {object_name}")