from metadata_extraction.dataset_discovery import list_parquet_objects
from metadata_extraction.schema_extractor import extract_schema_metadata


def aggregate_datasets(bucket_name="raw"):
    """
    Aggregate metadata from multiple parquet files
    into one logical dataset.
    """

    parquet_files = list_parquet_objects(bucket_name)

    aggregated = {}

    for file in parquet_files:

        parquet_path = f"s3://{bucket_name}/{file}"

        metadata = extract_schema_metadata(parquet_path)

        name = metadata.dataset_name

        if name not in aggregated:
            aggregated[name] = metadata

        else:
            existing_dataset = aggregated[name]
            previous_row_count = existing_dataset.row_count

            existing_cols = {
                c.column_name: c
                for c in existing_dataset.columns
            }
            incoming_cols = {
                c.column_name: c
                for c in metadata.columns
            }

            # A column absent from a file is null for every row in that file.
            for column_name, existing_column in existing_cols.items():
                incoming_column = incoming_cols.get(column_name)
                if incoming_column is None:
                    existing_column.null_count += metadata.row_count
                else:
                    existing_column.null_count += incoming_column.null_count

            # A column introduced later was null for previous rows.
            for column_name, incoming_column in incoming_cols.items():
                if column_name not in existing_cols:
                    incoming_column.null_count += previous_row_count
                    existing_dataset.columns.append(incoming_column)

            existing_dataset.row_count += metadata.row_count
            existing_dataset.column_count = len(existing_dataset.columns)

    return list(aggregated.values())
