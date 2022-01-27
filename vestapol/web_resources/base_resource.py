from abc import ABC, abstractmethod
from pendulum import DateTime
import pathlib
from vestapol.api import api


class BaseResource(ABC):
    def __init__(
        self,
        name,
        base_url,
        endpoint,
        version,
        response_format_tag,
        external_data_format_tag,
        response_filename="data",
        query_params=None
    ):
        self.name = name
        self.base_url = base_url
        self.endpoint = endpoint
        self.version = version
        self.response_format_tag = response_format_tag
        self.external_data_format_tag = external_data_format_tag
        self.response_filename = response_filename
        self.query_params = query_params

    def load(self, destination):
        data = self.request_data()
        self.write_data(data, destination)
        return data

    def request_data(self):
        self.requested_at = DateTime.utcnow().replace(microsecond=0)
        return api.get_api_data(
            f"{self.base_url}{self.endpoint}", self.response_format_tag, self.query_params
        )

    @abstractmethod
    def write_data(self, data, destination):
        pass

    def get_response_root(self, format_tag):
        return pathlib.Path(
            self.name, format_tag, self.version, self.requested_at_hive_path
        )

    @property
    def response_target_prefix(self):
        self._response_target_prefix = self.get_response_root(self.response_format_tag)
        return self._response_target_prefix

    @property
    def requested_at_hive_path(self):
        return f'requested_at={self.requested_at.strftime("%Y-%m-%d %H:%M:%S")}'

    @staticmethod
    def get_hive_path(data_path):

        prefix_components = []
        for x in data_path:
            prefix_components.append(f"{x[0]}={x[1]}")

        hive_path = "/".join(prefix_components)

        return hive_path
