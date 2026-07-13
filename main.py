from pipeline.metadata_pipeline import run_metadata_pipeline
from pipeline.lineage_pipeline import run_lineage_pipeline
from graph_model.upload_to_graphdb import clear_repository


def main():

    clear_repository()

    print("========== Metadata Pipeline ==========")
    run_metadata_pipeline()

    print()

    run_lineage_pipeline()

    print("Knowledge graph successfully generated.")


if __name__ == "__main__":
    main()
