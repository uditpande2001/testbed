from marquez.client import MarquezClient
from graph_model.lineage_generator import generate_lineage_graph

client = MarquezClient()
jobs = client.get_jobs()

graph = generate_lineage_graph(jobs)

print(f"Triples: {len(graph)}")

graph.serialize(
    destination="metadata/lineage.ttl",
    format="turtle"
)

print("Lineage graph saved to metadata/lineage.ttl")