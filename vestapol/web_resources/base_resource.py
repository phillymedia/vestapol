from abc import ABC, abstractmethod
from datetime import datetime
import pathlib
from vestapol.api import api


class BaseResource(ABC):
    name: str
    base_url: str
    version: str
    response_format_tag: str
    external_data_format_tag: str
    response_filename: str

    def load(self, destination):
        data = self.extract_data()
        self.write_data(data, destination)
        return data

    def extract_data(self):
        self.requested_at = datetime.utcnow().replace(microsecond=0)
        return api.get_api_data(f'{self.base_url}{self.endpoint}', self.response_format_tag)

    @abstractmethod
    def write_data(self, data, destination):
        pass

    def get_response_root(self, format_tag):
        return pathlib.Path(self.name, format_tag, self.version, self.requested_at_hive_path)

    @property
    def response_target_prefix(self):
        self._response_target_prefix = self.get_response_root(
            self.response_format_tag)
        return self._response_target_prefix

    @property
    def requested_at_hive_path(self):
        return f'requested_at={self.requested_at.strftime("%Y-%m-%d %H:%M:%S")}'

    @staticmethod
    def get_hive_path(data_path):

        prefix_components = []
        for x in data_path:
            prefix_components.append(f'{x[0]}={x[1]}')

        hive_path = '/'.join(prefix_components)

        return hive_path
