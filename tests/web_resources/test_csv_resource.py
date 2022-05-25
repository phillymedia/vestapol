from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from pendulum import DateTime

from vestapol.web_resources import csv_resource


@pytest.fixture
def mock_csv_resource():
    base_url = "www.test.com"
    name = "dummy_resource"
    endpoint = "/dummy"
    version = "v99.9"
    has_header = True
    mock_csv_resource = csv_resource.CSVResource(
        name, base_url, endpoint, version, has_header
    )
    mock_csv_resource.requested_at = DateTime(1970, 1, 1)
    return mock_csv_resource


@patch("vestapol.writers.text_writer.write_text")
def test_write_data(mock, mock_csv_resource):
    data = "a string"
    destination = MagicMock()
    mock_csv_resource.write_data(data, destination)
    mock.assert_called_with(
        data,
        Path(
            "dummy_resource",
            "csv",
            "v99.9",
            "requested_at=1970-01-01 00:00:00",
            "data.csv",
        ),
        destination,
    )


@patch("vestapol.web_resources.csv_resource.CSVResource.write_header")
@patch("vestapol.web_resources.csv_resource.CSVResource.write_data")
@patch("vestapol.web_resources.csv_resource.CSVResource.request_data")
def test_load(mock1, mock2, mock3, mock_csv_resource):
    mock_response_data = "col1,col2"
    mock1.return_value = mock_response_data
    destination = MagicMock()

    data = mock_csv_resource.load(destination)
    assert data == mock_response_data
    mock1.assert_called()
    mock2.assert_called_with(mock_response_data, destination)
    mock3.assert_called_with(mock_response_data, destination)
