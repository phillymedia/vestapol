import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from pathlib import Path

from vestapol.web_resources import json_resource


class DummyJSONResource(json_resource.JSONResource):
    base_url = 'www.test.com'
    name = 'dummy_resource'
    endpoint = '/dummy'
    version = 'v99.9'
    requested_at = datetime(1970, 1, 1)

    def unnest_data(self, data):
        pass


@pytest.fixture
def mock_unnest_data():
    with patch(__name__+'.'+'DummyJSONResource.unnest_data') as _patched:
        yield _patched


@patch('vestapol.writers.json_writer.write_json')
def test_write_data(mock):
    data = {'key': 'value'}
    destination = MagicMock()
    DummyJSONResource().write_data(data, destination)
    mock.assert_called_with(data,
                            Path(
                                'dummy_resource',
                                'json',
                                'v99.9',
                                'requested_at=1970-01-01 00:00:00',
                                'data.json'
                            ),
                            destination
                            )


@patch('vestapol.writers.json_writer.write_json')
def test_write_dict_no_data_path(mock):
    resource = DummyJSONResource()
    destination = MagicMock()
    data = {'key': 'value'}

    resource.write_dict(data, destination)
    mock.assert_called_with(
        data=data,
        pathname=Path(
            'dummy_resource',
            'jsonl',
            'v99.9',
            'requested_at=1970-01-01 00:00:00',
            'data.json'
        ),
        destination=destination
    )


@patch('vestapol.writers.json_writer.write_json')
def test_write_dict_data_path(mock):
    resource = DummyJSONResource()
    destination = MagicMock()
    data = {'key': 'value'}
    data_path = [('keyA', 'value1'), ('keyB', 'value2')]
    resource.write_dict(data, destination, data_path=data_path)
    mock.assert_called_with(
        data=data,
        pathname=Path(
            'dummy_resource',
            'jsonl',
            'v99.9',
            'requested_at=1970-01-01 00:00:00',
            'keyA=value1',
            'keyB=value2',
            'data.json'
        ),
        destination=destination
    )


@patch('vestapol.writers.json_writer.write_jsonl')
def test_write_list_no_data_path(mock):
    resource = DummyJSONResource()
    destination = MagicMock()
    data = [{'key': 'value'}]

    resource.write_list(data, destination)
    mock.assert_called_with(
        data=data,
        pathname=Path(
            'dummy_resource',
            'jsonl',
            'v99.9',
            'requested_at=1970-01-01 00:00:00',
            'data.json'
        ),
        destination=destination
    )


@patch('vestapol.writers.json_writer.write_jsonl')
def test_write_list_no_data(mock):
    resource = DummyJSONResource()
    destination = MagicMock()
    data = [{'key': 'value'}]
    data_path = [('keyA', 'value1'), ('keyB', 'value2')]
    resource.write_list(
        data, destination, data_path=data_path)
    mock.assert_called_with(
        data=data,
        pathname=Path(
            'dummy_resource',
            'jsonl',
            'v99.9',
            'requested_at=1970-01-01 00:00:00',
            'keyA=value1',
            'keyB=value2',
            'data.json'
        ),
        destination=destination
    )


@patch('vestapol.web_resources.json_resource.JSONResource.write_data')
@patch('vestapol.web_resources.json_resource.JSONResource.extract_data')
def test_extract(mock1, mock2, mock_unnest_data):
    mock1.return_value = {'key': 'value'}
    destination = MagicMock()

    DummyJSONResource().load(destination)
    mock1.assert_called()
    mock2.assert_called_with({'key': 'value'}, destination)
    mock_unnest_data.assert_called_with({'key': 'value'}, destination)
