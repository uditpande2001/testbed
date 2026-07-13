# Schema Lineage Demo

This demo uses the real Kafka consumers as the baseline, then writes controlled
changed-schema batches through the same Parquet and OpenLineage path.

Run with Marquez, MinIO, and GraphDB running:

```powershell
python ingestion/kafka_consumers/raw_sensor_data_consumer.py
python ingestion/kafka_consumers/command_response_consumer.py
python main.py

python -m demo.run_changed_schema
python main.py
```

The changed-schema script reads the latest real `meter-data` and
`command-response` Parquet rows from MinIO, preserves their original columns, and
adds the demo columns. This keeps the demo focused on `addsColumn` lineage rather
than noisy removed-column differences.

The changed run adds these columns to both demo datasets:

- `run_location`: `University of Stuttgart`
- `department`: `IPVS`
- `building`: `38`

It also adds dataset-specific demo columns:

- `meter-data`: `demo_run_label`
- `command-response`: `operator_group`

If Kafka messages are unavailable during practice, you can create a synthetic
baseline with:

```powershell
python -m demo.run_baseline_schema
python main.py
python -m demo.run_changed_schema
python main.py
```

Use this SPARQL query in GraphDB:

```sparql
PREFIX ex: <http://metadata-platform.com/>

SELECT ?process ?runId ?columnName
WHERE {
  ?run a ex:DataCollectionRun ;
       ex:realizes ?process ;
       ex:runId ?runId .

  ?change a ex:SchemaChange ;
          ex:observedInRun ?run ;
          ex:addsColumn ?column .

  ?column ex:name ?columnName .
}
ORDER BY ?process ?columnName
```
