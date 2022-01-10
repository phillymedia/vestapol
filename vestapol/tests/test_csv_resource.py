from unittest.mock import MagicMock, patch
from datetime import datetime
from pathlib import Path

from vestapol.web_resources import csv_resource


class DummyCSVResource(csv_resource.CSVResource):
    base_url = 'www.test.com'
    name = 'dummy_resource'
    endpoint = '/dummy'
    version = 'v99.9'
    requested_at = datetime(1970, 1, 1)
    has_header = True


@patch('vestapol.writers.text_writer.write_text')
def test_write_data(mock):
    data = 'a string'
    destination = MagicMock()
    DummyCSVResource().write_data(data, destination)
    mock.assert_called_with(
        data,
        Path(
            'dummy_resource',
            'csv',
            'v99.9',
            'requested_at=1970-01-01 00:00:00',
            'data.csv'
        ),
        destination
    )


@patch('vestapol.web_resources.csv_resource.CSVResource.write_header')
@patch('vestapol.web_resources.csv_resource.CSVResource.write_data')
@patch('vestapol.web_resources.csv_resource.CSVResource.extract_data')
def test_load(mock1, mock2, mock3):
    mock_response_data = 'col1,col2'
    mock1.return_value = mock_response_data
    destination = MagicMock()

    data = DummyCSVResource().load(destination)
    assert data == mock_response_data
    mock1.assert_called()
    mock2.assert_called_with(mock_response_data, destination)
    mock3.assert_called_with(mock_response_data, destination)
