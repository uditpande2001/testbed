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

    try:
        events = client.get_lineage_events()
    except Exception as exc:
        print(f"Could not read Marquez schema events: {exc}")
        print("Continuing with process-level lineage only.")
        events = []

    print(f"Found {len(jobs)} jobs and {len(events)} lineage events")

    graph = generate_lineage_graph(jobs, events)

    output_file = "metadata/lineage.ttl"

    graph.serialize(
        destination=output_file,
        format="turtle"
    )

    print(f"Generated {output_file}")

    upload_ttl(output_file)

    print("Lineage pipeline completed.\n")
