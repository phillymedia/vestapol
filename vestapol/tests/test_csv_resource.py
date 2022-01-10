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


@patch('vestapol.writers.text_writer.write_text')
def test_write_api_data(mock):
    api_data = 'a string'
    destination = MagicMock()
    DummyCSVResource().write_data(api_data, destination)
    mock.assert_called_with(
        api_data,
        Path(
            'dummy_resource',
            'csv',
            'v99.9',
            'requested_at=1970-01-01 00:00:00',
            'data.csv'
        ),
        destination
    )
