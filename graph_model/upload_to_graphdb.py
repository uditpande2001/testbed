import requests

GRAPHDB_URL = (
    "http://localhost:7200/repositories/"
    "metadata-kg/statements"
)


def upload_ttl(ttl_file):
    """
    Upload a Turtle file to GraphDB.
    """

    with open(ttl_file, "rb") as f:

        response = requests.post(
            GRAPHDB_URL,
            headers={
                "Content-Type": "text/turtle"
            },
            data=f
        )

    if response.status_code in (200, 201, 204):

        print(f"Uploaded: {ttl_file}")

    else:

        print(
            f"Upload failed ({response.status_code})"
        )

        print(response.text)


if __name__ == "__main__":

    upload_ttl(
        "metadata/meter-data.ttl"
    )