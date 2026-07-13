import unittest
from unittest.mock import patch

import pandas as pd

from lineage.openlineage_emitter import (
    build_schema_facet,
    complete_run,
    dataframe_schema_fields,
    start_run,
)


class OpenLineageEmitterTest(unittest.TestCase):
    def test_emits_output_schema_facet(self):
        dataframe = pd.DataFrame([
            {"meterNumber": "M1", "voltage": 230.5},
        ])
        schema_facet = build_schema_facet(dataframe_schema_fields(dataframe))

        with patch("lineage.openlineage_emitter.client.emit") as emit:
            run_id = start_run(
                job_name="meter-data-pipeline",
                input_namespace="kafka",
                input_dataset="raw-sensor-data",
                output_namespace="minio",
                output_dataset="meter-data",
                output_dataset_facets=schema_facet,
            )
            complete_run(
                run_id=run_id,
                job_name="meter-data-pipeline",
                input_namespace="kafka",
                input_dataset="raw-sensor-data",
                output_namespace="minio",
                output_dataset="meter-data",
                output_dataset_facets=schema_facet,
            )

        complete_event = emit.call_args_list[-1].args[0]
        fields = complete_event.outputs[0].facets["schema"]["fields"]

        self.assertEqual(run_id, complete_event.run.runId)
        self.assertEqual([field["name"] for field in fields], ["meterNumber", "voltage"])


if __name__ == "__main__":
    unittest.main()
