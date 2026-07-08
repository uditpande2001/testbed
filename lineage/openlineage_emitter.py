import uuid
from datetime import datetime, timezone

from openlineage.client import OpenLineageClient
from openlineage.client.run import (
    Dataset,
    Job,
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
            Dataset(
                namespace=input_namespace,
                name=input_dataset,
            )
        ],
        outputs=[
            Dataset(
                namespace=output_namespace,
                name=output_dataset,
            )
        ],
        producer="https://github.com/your-project/metadata-testbed",
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
    )

    return run_id


def complete_run(
    run_id: str,
    job_name: str,
    input_namespace: str,
    input_dataset: str,
    output_namespace: str,
    output_dataset: str,
):

    _emit_event(
        event_type=RunState.COMPLETE,
        run_id=run_id,
        job_name=job_name,
        input_namespace=input_namespace,
        input_dataset=input_dataset,
        output_namespace=output_namespace,
        output_dataset=output_dataset,
    )


def fail_run(
    run_id: str,
    job_name: str,
    input_namespace: str,
    input_dataset: str,
    output_namespace: str,
    output_dataset: str,
):

    _emit_event(
        event_type=RunState.FAIL,
        run_id=run_id,
        job_name=job_name,
        input_namespace=input_namespace,
        input_dataset=input_dataset,
        output_namespace=output_namespace,
        output_dataset=output_dataset,
    )