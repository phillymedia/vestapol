from __future__ import annotations

from abc import abstractmethod
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Generator
from typing import TYPE_CHECKING

from vestapol.web_resources import base_resource
from vestapol.writers import json_writer

if TYPE_CHECKING:
    from vestapol.destinations.base_destination import BaseDestination


class JSONResource(base_resource.BaseResource):
    response_format_tag = "json"
    external_data_format_tag = "jsonl"
    response_filename = "data.json"

    def __init__(
        self,
        name,
        base_url,
        endpoint,
        version,
        query_params=None,
        request_headers=None,
        manual_schema=None,
    ):
        self.name: str = name
        self.base_url: str = base_url
        self.endpoint: str = endpoint
        self.version: str = version
        self.query_params: Optional[dict] = query_params
        self.request_headers: Optional[dict] = request_headers
        self.manual_schema: Optional[List[Dict]] = manual_schema
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
            self.manual_schema,
        )

    def load(self, destination: BaseDestination):
        data = self.request_data()
        self.write_data(data, destination)
        self.unnest_data(data, destination)
        return data

    def write_data(self, api_data, destination: BaseDestination):
        json_writer.write_json(
            api_data, self.response_target_prefix / self.response_filename, destination
        )

    @abstractmethod
    def unnest_data(self, data, destination):
        pass

    def write_list(
        self,
        data: List[Dict],
        destination: BaseDestination,
        data_path: List[Tuple[str, Any]] = None,
    ):
        if not (isinstance(data, list) or isinstance(data, Generator)):
            raise TypeError(f"Expected a list or generator, received {type(data)}")

        pathname = self.get_pathname(data_path)
        json_writer.write_jsonl(data=data, pathname=pathname, destination=destination)

    def write_dict(
        self,
        data: Dict,
        destination: BaseDestination,
        data_path: List[Tuple[str, Any]] = None,
    ):
        if not isinstance(data, dict):
            raise TypeError(f"Expected a dict, received {type(data)}")

        pathname = self.get_pathname(data_path)
        json_writer.write_json(data=data, pathname=pathname, destination=destination)
