import hashlib
import json
from urllib.parse import quote

from rdflib import Graph, Literal, RDF, URIRef, XSD

from graph_model.namespaces import EX


def generate_lineage_graph(jobs, events=None):
    """
    Generate compact RDF lineage from Marquez topology and schema events.

    The graph intentionally avoids dumping every Marquez dataset-version UUID.
    It keeps the useful explanation layer: process, run, schema version, and
    schema changes such as added/removed/changed columns.
    """

    graph = Graph()
    graph.bind("ex", EX)

    for job in jobs:
        _add_job_topology(graph, job)

    previous_schemas = {}

    for event in sorted(events or [], key=lambda item: item.get("eventTime", "")):
        if event.get("eventType") != "COMPLETE":
            continue

        _add_schema_event(graph, event, previous_schemas)

    return graph


def _add_job_topology(graph, job):
    process_uri = _process_uri(job["name"])

    graph.add((process_uri, RDF.type, EX.DataCollectionProcess))
    graph.add((process_uri, EX.name, Literal(job["name"])))

    for dataset in job.get("inputs", []):
        dataset_uri = _add_dataset(graph, dataset)
        graph.add((process_uri, EX.consumes, dataset_uri))

    for dataset in job.get("outputs", []):
        dataset_uri = _add_dataset(graph, dataset)
        graph.add((process_uri, EX.creates, dataset_uri))

    return process_uri


def _add_schema_event(graph, event, previous_schemas):
    job = event.get("job") or {}
    run = event.get("run") or {}
    job_name = job.get("name")
    run_id = run.get("runId")

    if not job_name or not run_id:
        return

    process_uri = _add_job_topology(graph, job)
    run_uri = URIRef(f"{process_uri}/run/{_component(run_id)}")

    graph.add((run_uri, RDF.type, EX.DataCollectionRun))
    graph.add((run_uri, EX.realizes, process_uri))
    graph.add((run_uri, EX.runId, Literal(run_id)))

    if event_time := event.get("eventTime"):
        graph.add((run_uri, EX.eventTime, Literal(event_time, datatype=XSD.dateTime)))

    for dataset in event.get("outputs", []):
        schema_fields = _schema_fields(dataset)
        if not schema_fields:
            continue

        dataset_uri = _add_dataset(graph, dataset)
        graph.add((run_uri, EX.creates, dataset_uri))

        schema_uri, columns = _add_schema_version(graph, dataset_uri, schema_fields)
        graph.add((run_uri, EX.producedSchemaVersion, schema_uri))

        dataset_key = str(dataset_uri)
        previous_schema = previous_schemas.get(dataset_key)
        _add_schema_change(
            graph,
            run_uri,
            current_schema_uri=schema_uri,
            current_columns=columns,
            previous_schema=previous_schema,
        )
        previous_schemas[dataset_key] = (schema_uri, columns)


def _add_dataset(graph, dataset):
    namespace = dataset["namespace"]
    name = dataset["name"]
    dataset_uri = _dataset_uri(namespace, name)

    graph.add((dataset_uri, RDF.type, EX.DataRepresentation))
    graph.add((dataset_uri, EX.name, Literal(name)))

    return dataset_uri


def _add_schema_version(graph, dataset_uri, fields):
    fingerprint = _schema_fingerprint(fields)
    schema_uri = URIRef(f"{dataset_uri}/schema/{fingerprint}")

    graph.add((schema_uri, RDF.type, EX.SchemaVersion))
    graph.add((schema_uri, EX.schemaOf, dataset_uri))
    graph.add((schema_uri, EX.schemaFingerprint, Literal(fingerprint)))
    graph.add((dataset_uri, EX.hasSchemaVersion, schema_uri))

    columns = {}

    for field in fields:
        column_name = field["name"]
        column_type = field.get("type")
        column_uri = URIRef(f"{schema_uri}/column/{_component(column_name)}")

        graph.add((column_uri, RDF.type, EX.Column))
        graph.add((column_uri, EX.name, Literal(column_name)))
        graph.add((schema_uri, EX.hasColumn, column_uri))

        if column_type is not None:
            graph.add((column_uri, EX.dataType, Literal(column_type)))

        if ordinal_position := field.get("ordinal_position"):
            graph.add((
                column_uri,
                EX.ordinalPosition,
                Literal(ordinal_position, datatype=XSD.integer),
            ))

        columns[column_name] = (column_uri, column_type)

    return schema_uri, columns


def _add_schema_change(
    graph,
    run_uri,
    current_schema_uri,
    current_columns,
    previous_schema,
):
    if previous_schema is None:
        return

    previous_schema_uri, previous_columns = previous_schema

    if previous_schema_uri == current_schema_uri:
        return

    change_uri = URIRef(
        f"{run_uri}/schema-change/{current_schema_uri.rsplit('/', 1)[-1]}"
    )

    graph.add((change_uri, RDF.type, EX.SchemaChange))
    graph.add((change_uri, EX.observedInRun, run_uri))
    graph.add((change_uri, EX.previousSchemaVersion, previous_schema_uri))
    graph.add((change_uri, EX.nextSchemaVersion, current_schema_uri))

    for name, (column_uri, column_type) in current_columns.items():
        if name not in previous_columns:
            graph.add((change_uri, EX.addsColumn, column_uri))
        elif previous_columns[name][1] != column_type:
            graph.add((change_uri, EX.changesColumn, column_uri))
            graph.add((column_uri, EX.replacesColumn, previous_columns[name][0]))

    for name, (column_uri, _) in previous_columns.items():
        if name not in current_columns:
            graph.add((change_uri, EX.removesColumn, column_uri))


def _schema_fields(dataset):
    fields = ((dataset.get("facets") or {}).get("schema") or {}).get("fields") or []
    normalized = []

    for position, field in enumerate(fields, start=1):
        if field.get("name") is None:
            continue

        normalized_field = {
            "name": str(field["name"]),
            "ordinal_position": int(field.get("ordinal_position") or position),
        }

        if field.get("type") is not None:
            normalized_field["type"] = str(field["type"])

        normalized.append(normalized_field)

    return sorted(
        normalized,
        key=lambda field: (field.get("ordinal_position", 0), field["name"]),
    )


def _schema_fingerprint(fields):
    payload = json.dumps(fields, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _dataset_uri(namespace, name):
    return URIRef(
        f"{EX}data-representation/{_component(namespace)}/{_component(name)}"
    )


def _process_uri(job_name):
    return URIRef(f"{EX}data-collection-process/{_component(job_name)}")


def _component(value):
    return quote(str(value), safe="")
