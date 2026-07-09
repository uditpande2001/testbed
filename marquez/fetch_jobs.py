import requests

BASE = "http://localhost:5000/api/v1"

jobs = requests.get(
    f"{BASE}/namespaces/metadata-testbed/jobs"
).json()["jobs"]
# print(jobs)