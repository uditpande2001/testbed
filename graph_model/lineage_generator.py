from rdflib import Graph, RDF, URIRef

from graph_model.namespaces import EX


def generate_lineage_graph(jobs):
    """
    Generate RDF lineage from Marquez jobs.

    Marquez is the single source of truth for lineage.
    """

    graph = Graph()

    for job in jobs:

        process_uri = URIRef(
            EX + f"data-collection-process/{job['name']}"
        )

        graph.add((
            process_uri,
            RDF.type,
            EX.DataCollectionProcess
        ))

        #
        # Inputs
        #

        for dataset in job["inputs"]:

            dataset_uri = URIRef(
                EX +
                f"data-representation/"
                f"{dataset['namespace']}/"
                f"{dataset['name']}"
            )

            graph.add((
                dataset_uri,
                RDF.type,
                EX.DataRepresentation
            ))

            graph.add((
                process_uri,
                EX.consumes,
                dataset_uri
            ))

        #
        # Outputs
        #

        for dataset in job["outputs"]:

            dataset_uri = URIRef(
                EX +
                f"data-representation/"
                f"{dataset['namespace']}/"
                f"{dataset['name']}"
            )

            graph.add((
                dataset_uri,
                RDF.type,
                EX.DataRepresentation
            ))

            graph.add((
                process_uri,
                EX.creates,
                dataset_uri
            ))

    return graph