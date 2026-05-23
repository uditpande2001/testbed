

from kafka import KafkaConsumer

import json
import logging

from configs.kakfa_config import (
KAFKA_BOOTSTRAP_SERVERS, AUTO_OFFSET_RESET )


from configs.pipeline_config import (
    BATCH_SIZE,
    RAW_BUCKET
)

from storage.lakehouse.parquet_writer import (
    upload_batch_to_lake
)


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()


def kafka_consumer():

    consumer = KafkaConsumer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset=AUTO_OFFSET_RESET,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    consumer.subscribe(['command-response'])

    batch_messages = []

    for message in consumer:

        data = message.value

        batch_messages.append(data)

        if len(batch_messages) >= BATCH_SIZE:
            upload_batch_to_lake(
                messages=batch_messages,
                bucket_name=RAW_BUCKET,
                dataset_name="command-response"
            )

            batch_messages.clear()


if __name__ == '__main__':
    kafka_consumer()