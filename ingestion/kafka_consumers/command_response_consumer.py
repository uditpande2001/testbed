import datetime
from kafka import KafkaConsumer
import json
import os
import logging
from datetime import date, datetime

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def kafka_consumer():
    consumer = KafkaConsumer(
        bootstrap_servers='216.48.180.61:9092',
        auto_offset_reset='latest',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))

    )
    consumer.subscribe(['command-response'])

    for message in consumer:
        print(message)



if __name__ == '__main__':
    kafka_consumer()