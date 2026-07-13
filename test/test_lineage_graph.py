import unittest

from rdflib import Literal, RDF, URIRef

from graph_model.lineage_generator import generate_lineage_graph
from graph_model.namespaces import EX


def complete_event(run_id, fields):
    return {
        "eventTime": f"2026-07-13T10:00:0{run_id[-1]}Z",
        "eventType": "COMPLETE",
        "run": {"runId": run_id},
        "job": {
            "namespace": "metadata-testbed",
            "name": "meter-data-pipeline",
        },
        "inputs": [
            {"namespace": "kafka", "name": "raw-sensor-data"},
        ],
        "outputs": [
            {
                "namespace": "minio",
                "name": "meter-data",
                "facets": {
                    "schema": {
                        "fields": fields,
                    }
                },
            }
        ],
    }


class LineageGraphTest(unittest.TestCase):
    def test_schema_change_records_added_columns_without_dataset_versions(self):
        first_fields = [
            {"name": "meterNumber", "type": "object", "ordinal_position": 1},
        ]
        second_fields = [
            {"name": "meterNumber", "type": "object", "ordinal_position": 1},
            {"name": "voltage", "type": "float64", "ordinal_position": 2},
        ]

        graph = generate_lineage_graph(
            jobs=[],
            events=[
                complete_event("run-1", first_fields),
                complete_event("run-2", second_fields),
            ],
        )

        dataset_uri = URIRef(f"{EX}data-representation/minio/meter-data")

        self.assertIn((dataset_uri, EX.name, Literal("meter-data")), graph)
        self.assertIn((None, RDF.type, EX.DataCollectionRun), graph)
        self.assertIn((None, RDF.type, EX.SchemaVersion), graph)
        self.assertIn((None, RDF.type, EX.SchemaChange), graph)
        self.assertIn((None, EX.addsColumn, None), graph)
        self.assertNotIn((dataset_uri, EX.hasVersion, None), graph)


if __name__ == "__main__":
    unittest.main()
