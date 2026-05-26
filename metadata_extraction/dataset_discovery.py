from storage.lakehouse.minio_client import client

def list_parquet_objects(bucket_name):

    parquet_files = []

    objects = client.list_objects(
        bucket_name,
        recursive=True
    )

    for obj in objects:

        if obj.object_name.endswith(".parquet"):

            parquet_files.append(obj.object_name)

    return parquet_files

if __name__ == '__main__':

    parquet_files = list_parquet_objects("raw")

    for file in parquet_files:
        pass
        # print(file)
