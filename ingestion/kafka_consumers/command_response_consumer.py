from kafka import KafkaConsumer

import json
import logging
import signal

from datetime import datetime, timedelta

from configs.kakfa_config import (
    KAFKA_BOOTSTRAP_SERVERS,
    AUTO_OFFSET_RESET
)

from configs.pipeline_config import (
    BATCH_SIZE,
    RAW_BUCKET,
    RUN_DURATION_SECONDS
)

from storage.lakehouse.parquet_writer import (
    upload_batch_to_lake
)

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

shutdown_requested = False


def handle_shutdown(signum, frame):
    global shutdown_requested

    logger.info(f"Shutdown signal received: {signum}")
    shutdown_requested = True


signal.signal(signal.SIGINT, handle_shutdown)
signal.signal(signal.SIGTERM, handle_shutdown)


def flush_batch(batch_messages):

    if not batch_messages:
        return

    logger.info(f"Flushing remaining {len(batch_messages)} messages")

    upload_batch_to_lake(
        messages=batch_messages,
        bucket_name=RAW_BUCKET,
        dataset_name="command-response",
        source_name="command-response",
    )

    batch_messages.clear()


def kafka_consumer():

    consumer = KafkaConsumer(
        "command-response",
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset=AUTO_OFFSET_RESET,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        enable_auto_commit=True,
    )

    batch_messages = []

    logger.info("Command response consumer started")

    end_time = datetime.now() + timedelta(
        seconds=RUN_DURATION_SECONDS
    )

    try:

        while (
            not shutdown_requested
            and datetime.now() < end_time
        ):

            message_pack = consumer.poll(timeout_ms=1000)

            for _, messages in message_pack.items():

                for message in messages:

                    batch_messages.append(message.value)

                    if len(batch_messages) >= BATCH_SIZE:

                        upload_batch_to_lake(
                            messages=batch_messages,
                            bucket_name=RAW_BUCKET,
                            dataset_name="command-response",
                            source_name="command-response",
                        )

                        batch_messages.clear()

        logger.info("Run duration reached. Stopping consumer...")

    except Exception as e:

        logger.exception(f"Consumer error: {e}")

    finally:

        logger.info("Shutting down consumer")

        flush_batch(batch_messages)

        consumer.close()

        logger.info("Consumer closed successfully")


if __name__ == "__main__":
    kafka_consumer()