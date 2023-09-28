from unittest.mock import MagicMock
from unittest.mock import patch

from google.cloud import bigquery

from vestapol.destinations.gcp_destination import GoogleCloudPlatform


@patch("vestapol.destinations.gcp_destination.external_tables.create_gcp_table")
def test_create_table(mock):
    resource = MagicMock(
        external_data_format_tag="dum",
        version="v999.9",
        response_filename="dum.my",
        manual_schema=[
            {"name": "1a", "field_type": "INTEGER"},
            {"name": "1b", "field_type": "STRING"},
            {
                "name": "1c",
                "field_type": "RECORD",
                "fields": [
                    {"name": "2a", "field_type": "FLOAT64"},
                    {"name": "2b", "field_type": "INT64"},
                    {
                        "name": "2c",
                        "field_type": "RECORD",
                        "fields": [
                            {"name": "3a", "field_type": "INT64"},
                            {"name": "3b", "field_type": "STRING"},
                        ],
                    },
                ],
            },
        ],
    )

    resource.skip_leading_rows = 123
    resource.allow_quoted_newlines = True

    # Can't set the "name" attribute when instantiating a MagicMock
    resource.name = "dummy_resource"

    destination = GoogleCloudPlatform(
        "bucket_name", "root_prefix", "project_id", "dataset_id", "dataset_location"
    )

    tablename = destination.create_table(resource)

    assert tablename == "project_id.dataset_id.dummy_resource"

    mock.assert_called_with(
        "dum",
        "project_id",
        "dataset_id",
        "dataset_location",
        "dummy_resource",
        "gs://bucket_name/root_prefix/dummy_resource/dum/v999.9/",
        ["gs://bucket_name/root_prefix/dummy_resource/dum/v999.9/*/dum.my"],
        [
            bigquery.SchemaField("1a", "INTEGER"),
            bigquery.SchemaField("1b", "STRING"),
            bigquery.SchemaField(
                "1c",
                "RECORD",
                fields=[
                    bigquery.SchemaField("2a", "FLOAT64"),
                    bigquery.SchemaField("2b", "INT64"),
                    bigquery.SchemaField(
                        "2c",
                        "RECORD",
                        fields=[
                            bigquery.SchemaField("3a", "INT64"),
                            bigquery.SchemaField("3b", "STRING"),
                        ],
                    ),
                ],
            ),
        ],
        123,
        True,
    )
