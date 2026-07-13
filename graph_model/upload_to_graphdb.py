import requests
from pathlib import Path

GRAPHDB_URL = (
    "http://localhost:7200/repositories/"
    "metadata-kg/statements"
)

BASE_DIR = Path(__file__).resolve().parent.parent


def clear_repository():
    """
    Remove existing triples so GraphDB reflects the latest generated TTL files.
    """

    response = requests.delete(GRAPHDB_URL)

    if response.status_code in (200, 204):

        print("Cleared GraphDB repository")

    else:

        print(
            f"Clear failed ({response.status_code})"
        )

        print(response.text)


def upload_ttl(ttl_file):
    """
    Upload a Turtle file to GraphDB.
    """


    with open(BASE_DIR / ttl_file, "rb") as f:

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

    ttl_files = [
        "metadata/meter-data.ttl",
        "metadata/command-response.ttl",
        "metadata/lineage.ttl"
    ]

    for ttl_file in ttl_files:
        upload_ttl(ttl_file)
