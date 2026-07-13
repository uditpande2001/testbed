from __future__ import annotations

from metadata_extraction.dataset_discovery import list_parquet_objects
from metadata_extraction.parquet_reader import read_parquet_from_minio
from storage.lakehouse.parquet_writer import upload_batch_to_lake


BUCKET_NAME = "raw"
DEMO_CONTEXT_COLUMNS = {
    "run_location": "University of Stuttgart",
    "department": "IPVS",
    "building": "38",
}


def latest_messages_from_lake(dataset_name, row_count=2):
    """
    Read the latest real Parquet object for a dataset and return sample rows.
    """

    parquet_objects = [
        object_name
        for object_name in list_parquet_objects(BUCKET_NAME)
        if object_name.startswith(f"{dataset_name}/")
    ]

    if not parquet_objects:
        raise RuntimeError(
            f"No existing Parquet files found for {dataset_name}. "
            "Run the real Kafka consumer first to create the baseline."
        )

    latest_object = sorted(parquet_objects)[-1]
    dataframe = read_parquet_from_minio(f"s3://{BUCKET_NAME}/{latest_object}")

    if dataframe.empty:
        raise RuntimeError(
            f"Latest Parquet file for {dataset_name} is empty: {latest_object}"
        )

    return (
        dataframe.head(row_count)
        .where(dataframe.notnull(), None)
        .to_dict(orient="records")
    )


def add_demo_context(messages, extra_columns):
    return [
        {
            **message,
            **DEMO_CONTEXT_COLUMNS,
            **extra_columns,
        }
        for message in messages
    ]


def meter_data_baseline_messages():
    return [
        {
            "uuid": "demo-meter-001",
            "meterNumber": "M-STG-001",
            "nodeId": "node-38-a",
            "sensor_time": "2026-07-13T10:00:00Z",
            "meter_type": "electricity",
            "meter_category": "campus",
            "data": 230.4,
            "dataTypes": "voltage",
            "scalar": 1.0,
        },
        {
            "uuid": "demo-meter-002",
            "meterNumber": "M-STG-002",
            "nodeId": "node-38-b",
            "sensor_time": "2026-07-13T10:01:00Z",
            "meter_type": "electricity",
            "meter_category": "campus",
            "data": 229.8,
            "dataTypes": "voltage",
            "scalar": 1.0,
        },
    ]


def meter_data_changed_messages():
    return add_demo_context(
        latest_messages_from_lake("meter-data"),
        {"demo_run_label": "meter-data-schema-demo-v2"},
    )


def command_response_baseline_messages():
    return [
        {
            "commandId": "cmd-demo-001",
            "commandType": "CONNECT",
            "nodeId": "node-38-a",
            "status": "SUCCESS",
            "operationResults": "accepted",
            "debugServerTime": "2026-07-13T10:02:00Z",
        },
        {
            "commandId": "cmd-demo-002",
            "commandType": "READ_PROFILE",
            "nodeId": "node-38-b",
            "status": "SUCCESS",
            "operationResults": "queued",
            "debugServerTime": "2026-07-13T10:03:00Z",
        },
    ]


def command_response_changed_messages():
    return add_demo_context(
        latest_messages_from_lake("command-response"),
        {"operator_group": "campus-energy-lab"},
    )


def write_meter_data_baseline():
    upload_batch_to_lake(
        messages=meter_data_baseline_messages(),
        bucket_name=BUCKET_NAME,
        dataset_name="meter-data",
        source_name="raw-sensor-data",
    )


def write_meter_data_changed():
    upload_batch_to_lake(
        messages=meter_data_changed_messages(),
        bucket_name=BUCKET_NAME,
        dataset_name="meter-data",
        source_name="raw-sensor-data",
    )


def write_command_response_baseline():
    upload_batch_to_lake(
        messages=command_response_baseline_messages(),
        bucket_name=BUCKET_NAME,
        dataset_name="command-response",
        source_name="command-response",
    )


def write_command_response_changed():
    upload_batch_to_lake(
        messages=command_response_changed_messages(),
        bucket_name=BUCKET_NAME,
        dataset_name="command-response",
        source_name="command-response",
    )
