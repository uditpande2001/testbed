from metadata_extraction.dataset_discovery import (
    list_parquet_objects
)


def discover_datasets(bucket_name):

    parquet_files = list_parquet_objects(
        bucket_name
    )

    datasets = set()

    for file in parquet_files:

        dataset_name = file.split("/")[0]

        datasets.add(dataset_name)

    return sorted(list(datasets))


if __name__ == "__main__":

    datasets = discover_datasets("raw")

    print(datasets)