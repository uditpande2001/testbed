from minio import Minio

client = Minio(
    "localhost:9000",
    access_key="admin",
    secret_key="password123",
    secure=False
)

buckets = client.list_buckets()

for bucket in buckets:
    print(bucket.name)