from kafka import KafkaConsumer
from minio import Minio
import json
import logging
import pandas as pd

from datetime import datetime

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# setup minio datalake
minio_client = Minio(
    "localhost:9000",
    access_key="admin",
    secret_key="password123",
    secure=False
)

def upload_batch_to_lake(messages):

    if not messages:
        return

    # Convert batch to DataFrame
    df = pd.DataFrame(messages)

    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_name = f"meter_batch_{timestamp}.parquet"

    # Save locally temporarily
    df.to_parquet(file_name, index=False)

    # Date partitions
    today = datetime.now()

    object_name = (
        f"meter-data/"
        f"{today.year}/"
        f"{today.month:02}/"
        f"{today.day:02}/"
        f"{file_name}"
    )

    # Upload to MinIO raw bucket
    minio_client.fput_object(
        "raw",
        object_name,
        file_name
    )

    logger.info(f"Uploaded to lake: {object_name}")

# setup kafka consumer
def kafka_consumer():

    consumer = KafkaConsumer(
        bootstrap_servers='216.48.180.61:9092',
        auto_offset_reset='latest',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    consumer.subscribe(['raw-sensor-data'])

    batch_messages = []

    BATCH_SIZE = 100

    for message in consumer:

        data = message.value

        # print(data)

        batch_messages.append(data)

        # Upload batch when size reached
        if len(batch_messages) >= BATCH_SIZE:

            print("uploading to datalake")
            upload_batch_to_lake(batch_messages)

            batch_messages.clear()



if __name__ == '__main__':
    kafka_consumer()