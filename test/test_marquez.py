from marquez.client import MarquezClient

client = MarquezClient()

jobs = client.get_jobs()

for job in jobs:
    print(job["name"])

    for job in jobs:

        print("\nJOB:", job["name"])

        print("Inputs")

        for dataset in job["inputs"]:
            print("   ", dataset["namespace"], dataset["name"])

        print("Outputs")

        for dataset in job["outputs"]:
            print("   ", dataset["namespace"], dataset["name"])