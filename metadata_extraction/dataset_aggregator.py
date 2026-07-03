from collections import defaultdict

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
            # accumulate row counts
            aggregated[name].row_count += metadata.row_count

            # merge null counts column-wise
            existing_cols = {
                c.column_name: c
                for c in aggregated[name].columns
            }

            for col in metadata.columns:
                if col.column_name in existing_cols:
                    existing_cols[col.column_name].null_count += col.null_count

    return list(aggregated.values())