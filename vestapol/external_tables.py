from google.cloud import bigquery


def get_dataset(client, project_id, dataset_id, dataset_location):
    dataset = bigquery.Dataset(f"{project_id}.{dataset_id}")
    dataset.location = dataset_location
    dataset = client.create_dataset(dataset, exists_ok=True, timeout=30)
    return dataset


def get_external_data_configuration(source_uri_prefix_fq, source_uris, source_format):

    bq_source_format = {"jsonl": "NEWLINE_DELIMITED_JSON", "csv": "CSV"}[source_format]

    external_config = bigquery.ExternalConfig(bq_source_format)
    external_config.autodetect = True

    hive_partitioning_opts = bigquery.external_config.HivePartitioningOptions()
    hive_partitioning_opts.mode = "AUTO"
    hive_partitioning_opts.source_uri_prefix = source_uri_prefix_fq

    external_config.hive_partitioning = hive_partitioning_opts

    external_config.source_uris = source_uris

    if bq_source_format == "CSV":
        external_config.csv_options.skip_leading_rows = 1

    return external_config


def create_gcp_table(
    source_format,
    project_id,
    dataset_id,
    dataset_location,
    table_id,
    source_uri_prefix_fq,
    source_uris,
):

    client = bigquery.Client()
    dataset = get_dataset(client, project_id, dataset_id, dataset_location)

    # TODO: optionally create schema from header metadata

    table = bigquery.Table(dataset.table(table_id))

    table.external_data_configuration = get_external_data_configuration(
        source_uri_prefix_fq, source_uris, source_format
    )

    # Create a permanent table linked to the GCS file
    table = client.create_table(table, exists_ok=True)  # API request
