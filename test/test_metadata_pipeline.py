import unittest
from unittest.mock import patch

from metadata_extraction.dataset_aggregator import aggregate_datasets
from metadata_extraction.metadata_models import ColumnMetadata, DatasetMetadata


def metadata(row_count, columns):
    return DatasetMetadata(
        dataset_name="meter-data",
        parquet_path="s3://raw/meter-data/example.parquet",
        row_count=row_count,
        column_count=len(columns),
        source_type="kafka",
        source_name="raw-sensor-data",
        consumer_name="RawSensorDataConsumer",
        columns=[
            ColumnMetadata(name, data_type, null_count)
            for name, data_type, null_count in columns
        ],
    )


class MetadataAggregatorTest(unittest.TestCase):
    def test_columns_added_in_later_files_are_kept(self):
        with (
            patch(
                "metadata_extraction.dataset_aggregator.list_parquet_objects",
                return_value=["meter-data/a.parquet", "meter-data/b.parquet"],
            ),
            patch(
                "metadata_extraction.dataset_aggregator.extract_schema_metadata",
                side_effect=[
                    metadata(2, [("meterNumber", "object", 0)]),
                    metadata(
                        3,
                        [
                            ("meterNumber", "object", 1),
                            ("voltage", "float64", 0),
                        ],
                    ),
                ],
            ),
        ):
            [result] = aggregate_datasets()

        columns = {column.column_name: column for column in result.columns}

        self.assertEqual(result.row_count, 5)
        self.assertEqual(result.column_count, 2)
        self.assertEqual(columns["meterNumber"].null_count, 1)
        self.assertEqual(columns["voltage"].null_count, 2)


if __name__ == "__main__":
    unittest.main()
