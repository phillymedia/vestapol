import pytest
from unittest.mock import patch, MagicMock
from pendulum import DateTime
from pathlib import Path

from vestapol.web_resources import base_resource


class DummyBaseResource(base_resource.BaseResource):
    name = "dummy_resource"
    base_url = "www.test.com"
    endpoint = "/dummy"
    version = "v99.9"
    response_format_tag = "dum"
    external_data_format_tag = "duml"
    response_filename = "abc.txt"
    query_params = {"param1": "value1"}
    request_headers = {"header_key": "header_value"}
    requested_at = DateTime(1970, 1, 1)

    def write_data(self, data, destination):
        pass

    def __init__(self):
        super().__init__(
            self.name,
            self.base_url,
            self.endpoint,
            self.version,
            self.response_format_tag,
            self.external_data_format_tag,
            self.response_filename,
            self.query_params,
            self.request_headers,
            self.requested_at
        )


@pytest.fixture
def mock_write_data():
    with patch(__name__ + "." + "DummyBaseResource.write_data") as _patched:
        yield _patched


def test_resource():
    resource = DummyBaseResource()
    assert resource.response_target_prefix == Path(
        "dummy_resource", "dum", "v99.9", "requested_at=1970-01-01 00:00:00"
    )


@patch("vestapol.api.api.get_api_data")
def test_request_data(mock):
    DummyBaseResource().request_data()
    mock.assert_called_with("www.test.com/dummy", "dum", {"param1": "value1"}, {"header_key": "header_value"})


def test_get_hive_path():
    data_path = [("keyA", "value1"), ("keyB", "value2")]
    assert DummyBaseResource().get_hive_path(data_path) == "keyA=value1/keyB=value2"


@patch("vestapol.web_resources.base_resource.BaseResource.request_data")
def test_load(mock1, mock_write_data):
    mock_response_data = {"key": "value"}
    mock1.return_value = mock_response_data
    destination = MagicMock()
    data = DummyBaseResource().load(destination)

    assert data == mock_response_data
    mock1.assert_called()
    mock_write_data.assert_called_with(mock_response_data, destination)
