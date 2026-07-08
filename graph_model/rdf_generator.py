
from rdflib import Graph, RDF, Literal, URIRef

from graph_model.namespaces import EX



def generate_metadata_graph(dataset_metadata):
    """
    Generate an RDF metadata graph for a single logical dataset.

    Ontology mapping:
    - Kafka Topic            -> SourceBasedDataCollection
    - Kafka Consumer         -> DataCollectionProcess
    - Logical Dataset        -> DataRepresentation
    - Business Dataset       -> EnterpriseData
    - Extracted Metadata     -> MetadataCollection
    - Metadata Category      -> MetadataType (DataDescription)
    - MinIO                  -> StorageSystem
    """

    graph = Graph()

    # ------------------------------------------------------------------
    # URIs
    # ------------------------------------------------------------------

    enterprise_uri = URIRef(
        EX + "enterprise/probus"
    )

    enterprise_data_uri = URIRef(
        EX + f"enterprise-data/{dataset_metadata.dataset_name}"
    )

    data_representation_uri = URIRef(
        EX + f"data-representation/{dataset_metadata.dataset_name}"
    )

    metadata_collection_uri = URIRef(
        EX + f"metadata-collection/{dataset_metadata.dataset_name}"
    )

    source_collection_uri = URIRef(
        EX + f"source-based-data-collection/{dataset_metadata.source_name}"
    )

    data_collection_process_uri = URIRef(
        EX + f"data-collection-process/{dataset_metadata.consumer_name}"
    )

    storage_system_uri = URIRef(
        EX + "storage-system/minio"
    )

    data_description_uri = URIRef(
        EX + "metadata-type/data-description"
    )

    # ------------------------------------------------------------------
    # Enterprise
    # ------------------------------------------------------------------

    graph.add((
        enterprise_uri,
        RDF.type,
        EX.Enterprise
    ))

    graph.add((
        enterprise_uri,
        EX.hasDataCollection,
        source_collection_uri
    ))

    graph.add((
        enterprise_uri,
        EX.hasEnterpriseData,
        enterprise_data_uri
    ))

    graph.add((
        enterprise_uri,
        EX.hasStorageSystem,
        storage_system_uri
    ))

    # ------------------------------------------------------------------
    # Enterprise Data
    # ------------------------------------------------------------------

    graph.add((
        enterprise_data_uri,
        RDF.type,
        EX.EnterpriseData
    ))

    graph.add((
        enterprise_data_uri,
        EX.name,
        Literal(dataset_metadata.dataset_name)
    ))

    graph.add((
        enterprise_data_uri,
        EX.hasRepresentation,
        data_representation_uri
    ))

    graph.add((
        enterprise_data_uri,
        EX.hasMetadataCollection,
        metadata_collection_uri
    ))

    # ------------------------------------------------------------------
    # Source-Based Data Collection
    # ------------------------------------------------------------------

    graph.add((
        source_collection_uri,
        RDF.type,
        EX.SourceBasedDataCollection
    ))

    graph.add((
        source_collection_uri,
        EX.executedBy,
        data_collection_process_uri
    ))

    # ------------------------------------------------------------------
    # Data Collection Process
    # ------------------------------------------------------------------

    graph.add((
        data_collection_process_uri,
        RDF.type,
        EX.DataCollectionProcess
    ))

    graph.add((
        data_collection_process_uri,
        EX.creates,
        data_representation_uri
    ))

    # ------------------------------------------------------------------
    # Data Representation
    # ------------------------------------------------------------------

    graph.add((
        data_representation_uri,
        RDF.type,
        EX.DataRepresentation
    ))

    graph.add((
        data_representation_uri,
        EX.rowCount,
        Literal(dataset_metadata.row_count)
    ))

    graph.add((
        data_representation_uri,
        EX.columnCount,
        Literal(dataset_metadata.column_count)
    ))

    graph.add((
        data_representation_uri,
        EX.parquetPath,
        Literal(dataset_metadata.parquet_path)
    ))

    graph.add((
        data_representation_uri,
        EX.sourceName,
        Literal(dataset_metadata.source_name)
    ))

    graph.add((
        data_representation_uri,
        EX.consumerName,
        Literal(dataset_metadata.consumer_name)
    ))

    # ------------------------------------------------------------------
    # Storage System
    # ------------------------------------------------------------------

    graph.add((
        storage_system_uri,
        RDF.type,
        EX.StorageSystem
    ))

    graph.add((
        storage_system_uri,
        EX.stores,
        data_representation_uri
    ))

    # ------------------------------------------------------------------
    # Metadata Collection
    # ------------------------------------------------------------------

    graph.add((
        metadata_collection_uri,
        RDF.type,
        EX.MetadataCollection
    ))

    graph.add((
        metadata_collection_uri,
        EX.describes,
        data_representation_uri
    ))

    graph.add((
        metadata_collection_uri,
        EX.hasMetadataType,
        data_description_uri
    ))

    # ------------------------------------------------------------------
    # Metadata Type
    # ------------------------------------------------------------------

    graph.add((
        data_description_uri,
        RDF.type,
        EX.MetadataType
    ))

    graph.add((
        data_description_uri,
        EX.name,
        Literal("Data Description")
    ))

    # ------------------------------------------------------------------
    # Column Metadata
    # ------------------------------------------------------------------

    for column in dataset_metadata.columns:

        column_uri = URIRef(
            EX
            + f"data-representation/{dataset_metadata.dataset_name}/"
            + f"column/{column.column_name}"
        )

        graph.add((
            column_uri,
            RDF.type,
            EX.Column
        ))

        graph.add((
            data_representation_uri,
            EX.hasColumn,
            column_uri
        ))

        graph.add((
            column_uri,
            EX.dataType,
            Literal(column.data_type)
        ))

        graph.add((
            column_uri,
            EX.nullCount,
            Literal(column.null_count)
        ))

    return graph


