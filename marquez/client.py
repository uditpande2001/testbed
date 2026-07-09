import requests


class MarquezClient:
    def __init__(self, base_url="http://localhost:5000/api/v1"):
        self.base_url = base_url

    def get_jobs(self, namespace="metadata-testbed"):
        response = requests.get(
            f"{self.base_url}/namespaces/{namespace}/jobs"
        )
        response.raise_for_status()
        return response.json()["jobs"]