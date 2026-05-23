import json
import pandas as pd
from datetime import datetime
from minio import Minio
from minio import Minio

client = Minio(
    "localhost:9000",
    access_key="admin",
    secret_key="password123",
    secure=False
)

buckets = client.list_buckets()

for bucket in buckets:
    print(bucket.name)

def upload_batch_to_lake(messages):

    if not messages:
        return

    df = pd.DataFrame(messages)

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    file_name = f"meter_batch_{timestamp}.parquet"

    local_file = f"./{file_name}"

    # Save locally as parquet
    df.to_parquet(local_file, index=False)

    # Create date partition path
    today = datetime.now()

    object_name = (
        f"meter-data/"
        f"{today.year}/"
        f"{today.month:02}/"
        f"{today.day:02}/"
        f"{file_name}"
    )

    # Upload to MinIO
    client.fput_object(
        "raw",
        object_name,
        local_file
    )

    print(f"Uploaded: {object_name}")

sample_messages = [
        {
            "meter_id": 101,
            "power_consumption": 4.5,
            "timestamp": "2026-05-23T10:00:00"
        },
        {
            "meter_id": 102,
            "power_consumption": 3.2,
            "timestamp": "2026-05-23T10:01:00"
        }
    ]
upload_batch_to_lake(sample_messages)