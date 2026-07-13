import uuid
from datetime import datetime, timezone

from openlineage.client import OpenLineageClient
from openlineage.client.run import (
    InputDataset,
    Job,
    OutputDataset,
    Run,
    RunEvent,
    RunState,
)

# -------------------------------------------------------------------
# OpenLineage / Marquez Configuration
# -------------------------------------------------------------------

NAMESPACE = "metadata-testbed"

client = OpenLineageClient(
    url="http://localhost:5000"
)

SCHEMA_FACET_URL = (
    "https://openlineage.io/spec/facets/1-2-0/"
    "SchemaDatasetFacet.json#/$defs/SchemaDatasetFacet"
)

PRODUCER = "https://github.com/your-project/metadata-testbed"


def dataframe_schema_fields(dataframe):
    """
    Convert a pandas dataframe schema into OpenLineage schema fields.
    """

    return [
        {
            "name": str(column),
            "type": str(dataframe[column].dtype),
            "ordinal_position": position,
        }
        for position, column in enumerate(dataframe.columns, start=1)
    ]


def build_schema_facet(schema_fields):
    """
    Build the standard OpenLineage schema dataset facet.
    """

    return {
        "schema": {
            "_producer": PRODUCER,
            "_schemaURL": SCHEMA_FACET_URL,
            "fields": list(schema_fields),
        }
    }


# -------------------------------------------------------------------
# Internal helper
# -------------------------------------------------------------------

def _emit_event(
    event_type: RunState,
    run_id: str,
    job_name: str,
    input_namespace: str,
    input_dataset: str,
    output_namespace: str,
    output_dataset: str,
    input_dataset_facets=None,
    output_dataset_facets=None,
):
    """
    Emit a single OpenLineage event.
    """

    event = RunEvent(
        eventType=event_type,
        eventTime=datetime.now(timezone.utc).isoformat(),
        run=Run(runId=run_id),
        job=Job(
            namespace=NAMESPACE,
            name=job_name,
        ),
        inputs=[
            InputDataset(
                namespace=input_namespace,
                name=input_dataset,
                facets=input_dataset_facets or {},
            )
        ],
        outputs=[
            OutputDataset(
                namespace=output_namespace,
                name=output_dataset,
                facets=output_dataset_facets or {},
            )
        ],
        producer=PRODUCER,
    )

    client.emit(event)


# -------------------------------------------------------------------
# Public API
# -------------------------------------------------------------------

def start_run(
    job_name: str,
    input_namespace: str,
    input_dataset: str,
    output_namespace: str,
    output_dataset: str,
    input_dataset_facets=None,
    output_dataset_facets=None,
) -> str:

    run_id = str(uuid.uuid4())

    _emit_event(
        event_type=RunState.START,
        run_id=run_id,
        job_name=job_name,
        input_namespace=input_namespace,
        input_dataset=input_dataset,
        output_namespace=output_namespace,
        output_dataset=output_dataset,
        input_dataset_facets=input_dataset_facets,
        output_dataset_facets=output_dataset_facets,
    )

    return run_id


def complete_run(
    run_id: str,
    job_name: str,
    input_namespace: str,
    input_dataset: str,
    output_namespace: str,
    output_dataset: str,
    input_dataset_facets=None,
    output_dataset_facets=None,
):

    _emit_event(
        event_type=RunState.COMPLETE,
        run_id=run_id,
        job_name=job_name,
        input_namespace=input_namespace,
        input_dataset=input_dataset,
        output_namespace=output_namespace,
        output_dataset=output_dataset,
        input_dataset_facets=input_dataset_facets,
        output_dataset_facets=output_dataset_facets,
    )


def fail_run(
    run_id: str,
    job_name: str,
    input_namespace: str,
    input_dataset: str,
    output_namespace: str,
    output_dataset: str,
    input_dataset_facets=None,
    output_dataset_facets=None,
):

    _emit_event(
        event_type=RunState.FAIL,
        run_id=run_id,
        job_name=job_name,
        input_namespace=input_namespace,
        input_dataset=input_dataset,
        output_namespace=output_namespace,
        output_dataset=output_dataset,
        input_dataset_facets=input_dataset_facets,
        output_dataset_facets=output_dataset_facets,
    )
