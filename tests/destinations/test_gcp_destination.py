from unittest.mock import MagicMock
from unittest.mock import patch

from vestapol.destinations.gcp_destination import GoogleCloudPlatform


@patch("vestapol.destinations.gcp_destination.external_tables.create_gcp_table")
def test_create_table(mock):
    resource = MagicMock(
        external_data_format_tag="dum", version="v999.9", response_filename="dum.my"
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
    )
