from dataclasses import dataclass
from typing import List


@dataclass
class ColumnMetadata:

    column_name: str

    data_type: str

    null_count: int



@dataclass
class DatasetMetadata:

    dataset_name: str
    parquet_path: str

    row_count: int
    column_count: int

    source_type: str
    source_name: str
    consumer_name: str

    columns: List[ColumnMetadata]