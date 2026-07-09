from lineage.openlineage_emitter import emit_lineage

emit_lineage(
    namespace="testbed",
    job_name="RawSensorConsumer",
    input_dataset="raw-sensor-data",
    output_dataset="meter-data",
)

print("Lineage event sent.")