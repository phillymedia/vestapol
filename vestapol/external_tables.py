from typing import List
from typing import Optional

from google.cloud import bigquery


def get_dataset(
    client: bigquery.Client, project_id: str, dataset_id: str, dataset_location: str
):
    dataset = bigquery.Dataset(f"{project_id}.{dataset_id}")
    dataset.location = dataset_location
    dataset = client.create_dataset(dataset, exists_ok=True, timeout=30)
    return dataset


def get_external_data_configuration(
    source_uri_prefix_fq: str,
    source_uris: List[str],
    source_format: str,
    table_schema: Optional[List[bigquery.SchemaField]] = None,
    skip_leading_rows: int = 0,
    allow_quoted_newlines: Optional[bool] = False,
    specified_delimeter: Optional[str] =",",
):

    bq_source_format = {"jsonl": "NEWLINE_DELIMITED_JSON", "csv": "CSV"}[source_format]

    external_config = bigquery.ExternalConfig(bq_source_format)

    # autodetect schema unless a manually defined one is provided
    if table_schema is not None:
        external_config.schema = table_schema
    else:
        external_config.autodetect = True

    hive_partitioning_opts = bigquery.external_config.HivePartitioningOptions()
    hive_partitioning_opts.mode = "AUTO"
    hive_partitioning_opts.source_uri_prefix = source_uri_prefix_fq

    external_config.hive_partitioning = hive_partitioning_opts

    external_config.source_uris = source_uris

    if bq_source_format == "CSV":
        # skips mypy since Google does not give CSVOptions a signature
        external_config.csv_options.skip_leading_rows = skip_leading_rows  # type: ignore # noqa: E501
        external_config.csv_options.allow_quoted_newlines = allow_quoted_newlines  # type: ignore # noqa: E501
        external_config.csv_options.specified_delimiter = specified_delimeter

    return external_config


def create_gcp_table(
    source_format: str,
    project_id: str,
    dataset_id: str,
    dataset_location: str,
    table_id: str,
    source_uri_prefix_fq: str,
    source_uris: List[str],
    table_schema: Optional[List[bigquery.SchemaField]],
    skip_leading_rows: int = 0,
    allow_quoted_newlines: Optional[bool] = False,
    specified_delimeter: Optional[str] = ",",

):

    client = bigquery.Client()
    dataset = get_dataset(client, project_id, dataset_id, dataset_location)

    # TODO: optionally create schema from header metadata

    table = bigquery.Table(dataset.table(table_id))

    table.external_data_configuration = get_external_data_configuration(
        source_uri_prefix_fq,
        source_uris,
        source_format,
        table_schema,
        skip_leading_rows,
        allow_quoted_newlines,
        specified_delimeter,
    )

    # Create a permanent table linked to the GCS file
    table = client.create_table(table, exists_ok=True)  # API request
