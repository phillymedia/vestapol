from __future__ import annotations

import pathlib
from abc import ABC
from abc import abstractmethod
from typing import List, Tuple, Any, Optional, TYPE_CHECKING

from pendulum import DateTime

from vestapol.api import api

if TYPE_CHECKING:
    from vestapol.destinations import DestinationTypes


class BaseResource(ABC):
    def __init__(
        self,
        name: str,
        base_url: Optional[str],
        endpoint: Optional[str],
        version: str,
        response_format_tag: str,
        external_data_format_tag: str,
        response_filename: str = "data",
        query_params: dict = None,
        request_headers: dict = None,
        manual_schema=None,
    ):
        self.name = name
        self.base_url = base_url
        self.endpoint = endpoint
        self.version = version
        self.response_format_tag = response_format_tag
        self.external_data_format_tag = external_data_format_tag
        self.response_filename = response_filename
        self.query_params = query_params
        self.request_headers = request_headers
        self.manual_schema = manual_schema
        self.requested_at = DateTime.utcnow().replace(microsecond=0)

    def load(self, destination: DestinationTypes):
        data = self.request_data()
        self.write_data(data, destination)
        return data

    def request_data(self):
        return api.get_api_data(
            f"{self.base_url}{self.endpoint}",
            self.response_format_tag,
            self.query_params,
            self.request_headers,
        )

    @abstractmethod
    def write_data(self, data, destination: DestinationTypes):
        pass

    def get_response_root(self, format_tag: str):
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
    def get_hive_path(data_path: List[Tuple[str, Any]]) -> str:

        prefix_components = []
        for x in data_path:
            prefix_components.append(f"{x[0]}={x[1]}")

        hive_path = "/".join(prefix_components)

        return hive_path

    def get_pathname(self, data_path: List[Tuple[str, Any]] = None) -> str:
        target_prefix = self.get_response_root(self.external_data_format_tag)

        if data_path:
            hive_path = self.get_hive_path(data_path)
            pathname = target_prefix / hive_path / self.response_filename
        else:
            pathname = target_prefix / self.response_filename

        return pathname
