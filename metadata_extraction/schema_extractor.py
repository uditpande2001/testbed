from metadata_extraction.parquet_reader import (
    read_parquet_from_minio
)

from metadata_extraction.dataset_discovery import (
    list_parquet_objects
)

from metadata_extraction.metadata_models import (
    DatasetMetadata,
    ColumnMetadata
)


def extract_schema_metadata(parquet_path):

    df = read_parquet_from_minio(parquet_path)

    dataset_name = parquet_path.split("/")[3]

    columns = []

    for column in df.columns:

        column_metadata = ColumnMetadata(
            column_name=column,
            data_type=str(df[column].dtype),
            null_count=int(df[column].isnull().sum())
        )

        columns.append(column_metadata)

    dataset_metadata = DatasetMetadata(
        dataset_name=dataset_name,
        parquet_path=parquet_path,
        row_count=len(df),
        columns=columns
    )

    return dataset_metadata


if __name__ == '__main__':

    parquet_files = list_parquet_objects("raw")

    for file in parquet_files:

        parquet_path = f"s3://raw/{file}"

        print(f"\nProcessing: {parquet_path}")

        metadata = extract_schema_metadata(
            parquet_path
        )

        print("\nDataset:", metadata.dataset_name)

        print("Rows:", metadata.row_count)

        print("Columns:")

        for column in metadata.columns:
            print(
                f" - {column.column_name} "
                f"({column.data_type}) "
                f"nulls={column.null_count}"
            )