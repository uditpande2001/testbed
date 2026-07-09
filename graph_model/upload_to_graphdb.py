import requests
from pathlib import Path

GRAPHDB_URL = (
    "http://localhost:7200/repositories/"
    "metadata-kg/statements"
)

BASE_DIR = Path(__file__).resolve().parent.parent

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