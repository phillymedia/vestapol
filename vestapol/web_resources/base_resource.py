from __future__ import annotations

import pathlib
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import List
from typing import Optional
from typing import Tuple
from typing import TYPE_CHECKING

from pendulum import DateTime

from vestapol.api import api

if TYPE_CHECKING:
    from vestapol.destinations.base_destination import BaseDestination


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
        skip_leading_rows: int = 0,
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
        self.skip_leading_rows = skip_leading_rows

    def load(self, destination: BaseDestination):
        """The main entry point method for Vestapol resources. This method
        retrieves data from some external resource and then writes the data to a
        destination.

        Args:
            destination (BaseDestination): The destination being written to. See
            the destinations module for supported destination types.

        Returns:
            list: a list of data rows
        """
        data = self.request_data()
        self.write_data(data, destination)
        return data  # TODO: I think we can remove this return statement

    def request_data(self):
        """Method that encapsulates the call to an API or other web resource. It
        returns a raw representation of the response may be further transformed
        so that it can be parsed by external object tables. In most instances,
        this method will be overridden when creating a subclass of BaseResource.

        Returns:
            any: a representation of the data returned by the API call
        """
        return api.get_api_data(
            f"{self.base_url}{self.endpoint}",
            self.response_format_tag,
            self.query_params,
            self.request_headers,
        )

    @abstractmethod
    def write_data(self, data, destination: BaseDestination):
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
