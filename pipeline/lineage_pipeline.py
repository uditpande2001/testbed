from marquez.client import MarquezClient

from graph_model.lineage_generator import generate_lineage_graph
from graph_model.upload_to_graphdb import upload_ttl


def run_lineage_pipeline():
    """
    Retrieve lineage from Marquez, generate RDF,
    and upload it to GraphDB.
    """

    print("\n========== Lineage Pipeline ==========")

    client = MarquezClient()

    jobs = client.get_jobs()

    print(f"Found {len(jobs)} jobs")

    graph = generate_lineage_graph(jobs)

    output_file = "metadata/lineage.ttl"

    graph.serialize(
        destination=output_file,
        format="turtle"
    )

    print(f"Generated {output_file}")

    upload_ttl(output_file)

    print("Lineage pipeline completed.\n")