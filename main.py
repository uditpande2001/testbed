from pipeline.metadata_pipeline import run_metadata_pipeline
from pipeline.lineage_pipeline import run_lineage_pipeline


def main():

    print("========== Metadata Pipeline ==========")
    run_metadata_pipeline()

    print()

    run_lineage_pipeline()

    print("Knowledge graph successfully generated.")


if __name__ == "__main__":
    main()