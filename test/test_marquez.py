import unittest
from unittest.mock import Mock, patch

from marquez.client import MarquezClient


class MarquezClientTest(unittest.TestCase):
    def test_get_lineage_events_filters_namespace(self):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "totalCount": 2,
            "events": [
                {"job": {"namespace": "other"}, "run": {"runId": "ignored"}},
                {"job": {"namespace": "metadata-testbed"}, "run": {"runId": "run-1"}},
            ]
        }

        with patch("marquez.client.requests.get", return_value=response) as get:
            client = MarquezClient(base_url="http://marquez.test/api/v1")
            events = client.get_lineage_events()

        self.assertEqual([event["run"]["runId"] for event in events], ["run-1"])
        self.assertEqual(
            get.call_args.args[0],
            "http://marquez.test/api/v1/events/lineage",
        )
        self.assertEqual(get.call_args.kwargs["params"]["sortDirection"], "asc")

    def test_get_lineage_events_paginates_all_events(self):
        first_response = Mock()
        first_response.raise_for_status.return_value = None
        first_response.json.return_value = {
            "totalCount": 3,
            "events": [
                {"job": {"namespace": "metadata-testbed"}, "run": {"runId": "run-1"}},
                {"job": {"namespace": "metadata-testbed"}, "run": {"runId": "run-2"}},
            ],
        }
        second_response = Mock()
        second_response.raise_for_status.return_value = None
        second_response.json.return_value = {
            "totalCount": 3,
            "events": [
                {"job": {"namespace": "metadata-testbed"}, "run": {"runId": "run-3"}},
            ],
        }

        with patch(
            "marquez.client.requests.get",
            side_effect=[first_response, second_response],
        ) as get:
            client = MarquezClient(base_url="http://marquez.test/api/v1")
            events = client.get_lineage_events(limit=2)

        self.assertEqual(
            [event["run"]["runId"] for event in events],
            ["run-1", "run-2", "run-3"],
        )
        self.assertEqual(get.call_args_list[0].kwargs["params"]["offset"], 0)
        self.assertEqual(get.call_args_list[1].kwargs["params"]["offset"], 2)


if __name__ == "__main__":
    unittest.main()
