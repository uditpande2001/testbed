import requests


class MarquezClient:
    def __init__(self, base_url="http://localhost:5000/api/v1"):
        self.base_url = base_url.rstrip("/")

    def get_jobs(self, namespace="metadata-testbed"):
        response = requests.get(
            f"{self.base_url}/namespaces/{namespace}/jobs",
            timeout=10,
        )
        response.raise_for_status()
        return response.json()["jobs"]

    def get_lineage_events(self, namespace="metadata-testbed", limit=500):
        """
        Fetch recent OpenLineage events from Marquez and keep this namespace.
        """

        events = []
        offset = 0

        while True:
            response = requests.get(
                f"{self.base_url}/events/lineage",
                params={
                    "sortDirection": "asc",
                    "limit": limit,
                    "offset": offset,
                },
                timeout=10,
            )
            response.raise_for_status()

            payload = response.json()
            page = payload.get("events", [])

            events.extend(
                event
                for event in page
                if event.get("job", {}).get("namespace") == namespace
            )

            offset += len(page)
            total_count = payload.get("totalCount")

            if not page:
                return events

            if isinstance(total_count, int) and offset >= total_count:
                return events
