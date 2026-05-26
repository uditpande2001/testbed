from rdflib import Graph, RDF, Literal, URIRef

from graph_model.namespaces import EX

from metadata_extraction.schema_extractor import (
    extract_schema_metadata
)

from metadata_extraction.dataset_discovery import (
    list_parquet_objects
)

def generate_dataset_rdf(dataset_metadata):

    graph = Graph()

    # Dataset URI
    dataset_uri = URIRef(
        EX + f"dataset/{dataset_metadata.dataset_name}"
    )

    graph.add((
        dataset_uri,
        RDF.type,
        EX.Dataset
    ))

    graph.add((
        dataset_uri,
        EX.rowCount,
        Literal(dataset_metadata.row_count)
    ))

    # Columns
    for column in dataset_metadata.columns:


        column_uri = URIRef(
            EX +
            f"dataset/{dataset_metadata.dataset_name}/"
            f"column/{column.column_name}"
        )

        graph.add((
            column_uri,
            RDF.type,
            EX.Column
        ))

        graph.add((
            dataset_uri,
            EX.hasColumn,
            column_uri
        ))

        graph.add((
            column_uri,
            EX.dataType,
            Literal(column.data_type)
        ))

        graph.add((
            column_uri,
            EX.nullCount,
            Literal(column.null_count)
        ))

    return graph





if __name__ == '__main__':

    parquet_files = list_parquet_objects("raw")

    combined_graph = Graph()

    for file in parquet_files:
        parquet_path = f"s3://raw/{file}"

        # print(f"\nProcessing: {parquet_path}")

        metadata = extract_schema_metadata(
            parquet_path
        )

        rdf_graph = generate_dataset_rdf(
            metadata
        )

        combined_graph += rdf_graph

    print(
        combined_graph.serialize(format="turtle")
    )