from marquez.client import MarquezClient


def run_lineage_pipeline():

    client = MarquezClient()

    jobs = client.get_jobs()

    print(f"Found {len(jobs)} jobs")

    for job in jobs:

        print(f"\nJob: {job['name']}")

        print("Inputs:")

        for dataset in job["inputs"]:
            print(
                f"  {dataset['namespace']} -> {dataset['name']}"
            )

        print("Outputs:")

        for dataset in job["outputs"]:
            print(
                f"  {dataset['namespace']} -> {dataset['name']}"
            )

if __name__ == '__main__':
    run_lineage_pipeline()