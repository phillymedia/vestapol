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
            {"name": "test1", "field_type": "INTEGER"},
            {"name": "test2", "field_type": "STRING"},
            {
                "name": "test3",
                "field_type": "RECORD",
                "fields": [
                    {"name": "name", "field_type": "FLOAT64"},
                    {"name": "id", "field_type": "INT64"},
                ],
            },
        ],
        skip_leading_rows=123,
    )

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
            bigquery.SchemaField("test1", "INTEGER"),
            bigquery.SchemaField("test2", "STRING"),
            bigquery.SchemaField(
                "test3",
                "RECORD",
                fields=[
                    bigquery.SchemaField("name", "FLOAT64"),
                    bigquery.SchemaField("id", "INT64"),
                ],
            ),
        ],
        123,
    )
