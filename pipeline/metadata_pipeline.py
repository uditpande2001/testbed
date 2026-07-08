from metadata_extraction.dataset_aggregator import (
    aggregate_datasets
)

from graph_model.rdf_generator import (
    generate_metadata_graph
)

from graph_model.upload_to_graphdb import (
    upload_ttl
)

from lineage.openlineage_emitter import (
    start_run,
    complete_run,
    fail_run,
)


def run_metadata_pipeline():

    print("\nStarting metadata pipeline...")

    datasets = aggregate_datasets()

    print(f"Found {len(datasets)} datasets")

    for dataset in datasets:

        print(f"\nProcessing dataset: {dataset.dataset_name}")

        ttl_path = f"metadata/{dataset.dataset_name}.ttl"

        # ==========================================================
        # Job 1
        # Metadata Processing
        # ==========================================================

        processing_run = start_run(
            job_name="metadata-processing",

            input_namespace="minio",
            input_dataset=dataset.dataset_name,

            output_namespace="rdf",
            output_dataset=ttl_path,
        )

        try:

            graph = generate_metadata_graph(dataset)

            graph.serialize(
                destination=ttl_path,
                format="turtle"
            )

            complete_run(
                run_id=processing_run,

                job_name="metadata-processing",

                input_namespace="minio",
                input_dataset=dataset.dataset_name,

                output_namespace="rdf",
                output_dataset=ttl_path,
            )

            print(f"Generated {ttl_path}")

        except Exception:

            fail_run(
                run_id=processing_run,

                job_name="metadata-processing",

                input_namespace="minio",
                input_dataset=dataset.dataset_name,

                output_namespace="rdf",
                output_dataset=ttl_path,
            )

            raise

        # ==========================================================
        # Job 2
        # Knowledge Graph Loading
        # ==========================================================

        graphdb_run = start_run(
            job_name="knowledge-graph-loading",

            input_namespace="rdf",
            input_dataset=ttl_path,

            output_namespace="graphdb",
            output_dataset="metadata-kg",
        )

        try:

            upload_ttl(ttl_path)

            complete_run(
                run_id=graphdb_run,

                job_name="knowledge-graph-loading",

                input_namespace="rdf",
                input_dataset=ttl_path,

                output_namespace="graphdb",
                output_dataset="metadata-kg",
            )

            print("Uploaded to GraphDB")

        except Exception:

            fail_run(
                run_id=graphdb_run,

                job_name="knowledge-graph-loading",

                input_namespace="rdf",
                input_dataset=ttl_path,

                output_namespace="graphdb",
                output_dataset="metadata-kg",
            )

            raise

    print("\nMetadata pipeline completed successfully.")

    return datasets