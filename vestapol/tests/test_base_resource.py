import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from pathlib import Path

from vestapol.web_resources import base_resource


class DummyBaseResource(base_resource.BaseResource):
    base_url = 'www.test.com'
    name = 'dummy_resource'
    endpoint = '/dummy'
    response_format_tag = 'dum'
    version = 'v99.9'
    requested_at = datetime(1970, 1, 1)

    def write_data(self, data):
        pass


@pytest.fixture
def mock_write_data():
    with patch(__name__+'.'+'DummyBaseResource.write_data') as _patched:
        yield _patched


def test_resource():
    resource = DummyBaseResource()

    assert resource.response_target_prefix == Path(
        'dummy_resource',
        'dum',
        'v99.9',
        'requested_at=1970-01-01 00:00:00'
    )


@patch('vestapol.api.api.get_api_data')
def test_extract_data(mock):
    DummyBaseResource().extract_data()
    mock.assert_called_with('www.test.com/dummy', 'dum')


def test_get_hive_path():
    data_path = [('keyA', 'value1'), ('keyB', 'value2')]
    assert DummyBaseResource().get_hive_path(
        data_path) == 'keyA=value1/keyB=value2'


@patch('vestapol.web_resources.base_resource.BaseResource.extract_data')
def test_extract(mock1, mock_write_data):
    mock1.return_value = {'key': 'value'}
    destination = MagicMock()
    DummyBaseResource().load(destination)
    mock1.assert_called()
    mock_write_data.assert_called_with({'key': 'value'}, destination)
