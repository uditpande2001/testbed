import requests

GRAPHDB_URL = (
    "http://localhost:7200/repositories/"
    "metadata-kg/statements"
)

TTL_FILE = "metadata.ttl"


def upload_ttl():
    # Clear existing data
    response = requests.delete(GRAPHDB_URL)

    if response.status_code in (200, 204):
        print("Existing metadata cleared.")
    else:
        print(
            f"Warning: could not clear repository "
            f"({response.status_code})"
        )

    # Upload new metadata
    with open(TTL_FILE, "rb") as f:
        response = requests.post(
            GRAPHDB_URL,
            headers={
                "Content-Type": "text/turtle"
            },
            data=f
        )

    if response.status_code in (200, 201, 204):
        print("Metadata uploaded successfully.")
    else:
        print(
            f"Upload failed: {response.status_code}"
        )
        print(response.text)


if __name__ == "__main__":
    upload_ttl()