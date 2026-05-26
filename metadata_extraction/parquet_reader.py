import pandas as pd


def read_parquet_from_minio(parquet_path):

    df = pd.read_parquet(
        parquet_path,
        storage_options={
            "key": "admin",
            "secret": "password123",
            "client_kwargs": {
                "endpoint_url": "http://localhost:9000"
            }
        }
    )

    # print(df)
    return df