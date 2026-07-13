import unittest
from unittest.mock import patch

from demo import demo_batches


class DemoBatchesTest(unittest.TestCase):
    def test_changed_batches_add_demo_context_columns(self):
        with patch(
            "demo.demo_batches.latest_messages_from_lake",
            side_effect=[
                [{"meterNumber": "M-STG-001"}],
                [{"commandId": "cmd-demo-001"}],
            ],
        ):
            meter_message = demo_batches.meter_data_changed_messages()[0]
            command_message = demo_batches.command_response_changed_messages()[0]

        for message in (meter_message, command_message):
            self.assertEqual(message["run_location"], "University of Stuttgart")
            self.assertEqual(message["department"], "IPVS")
            self.assertEqual(message["building"], "38")

        self.assertIn("demo_run_label", meter_message)
        self.assertIn("operator_group", command_message)

    def test_demo_writers_use_existing_lakehouse_path(self):
        with (
            patch(
                "demo.demo_batches.latest_messages_from_lake",
                return_value=[{"meterNumber": "M-STG-001"}],
            ),
            patch("demo.demo_batches.upload_batch_to_lake") as upload,
        ):
            demo_batches.write_meter_data_changed()

        upload.assert_called_once()
        call = upload.call_args.kwargs

        self.assertEqual(call["bucket_name"], "raw")
        self.assertEqual(call["dataset_name"], "meter-data")
        self.assertEqual(call["source_name"], "raw-sensor-data")
        self.assertIn("run_location", call["messages"][0])

    def test_latest_messages_requires_real_baseline(self):
        with patch("demo.demo_batches.list_parquet_objects", return_value=[]):
            with self.assertRaisesRegex(RuntimeError, "Run the real Kafka consumer"):
                demo_batches.latest_messages_from_lake("meter-data")


if __name__ == "__main__":
    unittest.main()
