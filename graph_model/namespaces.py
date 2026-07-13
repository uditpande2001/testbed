from rdflib import Namespace

EX = Namespace("http://metadata-platform.com/")

# Classes
#
# Enterprise
# EnterpriseData
# DataRepresentation
# MetadataCollection
# MetadataType
# StorageSystem
# Column
# DataCollectionProcess
# DataCollectionRun
# SchemaVersion
# SchemaChange
#
# Properties
#
# hasEnterpriseData
# hasRepresentation
# hasStorageSystem
# hasMetadataCollection
# stores
# describes
# hasMetadataType
# hasColumn
# rowCount
# columnCount
# parquetPath
# dataType
# nullCount
# creates
# consumes
# name
# realizes
# runId
# eventTime
# hasSchemaVersion
# producedSchemaVersion
# schemaOf
# schemaFingerprint
# previousSchemaVersion
# nextSchemaVersion
# observedInRun
# addsColumn
# removesColumn
# changesColumn
# replacesColumn
# ordinalPosition
