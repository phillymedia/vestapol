from __future__ import annotations

from abc import abstractmethod
from typing import Dict, List, Tuple, Any, Optional, TYPE_CHECKING

from vestapol.web_resources import base_resource
from vestapol.writers import json_writer

if TYPE_CHECKING:
    from vestapol.destinations import DestinationTypes


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

    def load(self, destination: DestinationTypes):
        data = self.request_data()
        self.write_data(data, destination)
        self.unnest_data(data, destination)
        return data

    def write_data(self, api_data, destination: DestinationTypes):
        json_writer.write_json(
            api_data, self.response_target_prefix / self.response_filename, destination
        )

    @abstractmethod
    def unnest_data(self, data, destination):
        pass

    def write_list(
        self,
        data: List[Dict],
        destination: DestinationTypes,
        data_path: List[Tuple[str, Any]] = None,
    ):
        if not isinstance(data, list):
            raise TypeError(f"Expected a list, received {type(data)}")

        pathname = self.get_pathname(data_path)
        json_writer.write_jsonl(data=data, pathname=pathname, destination=destination)

    def write_dict(
        self,
        data: Dict,
        destination: DestinationTypes,
        data_path: List[Tuple[str, Any]] = None,
    ):
        if not isinstance(data, dict):
            raise TypeError(f"Expected a dict, received {type(data)}")

        pathname = self.get_pathname(data_path)
        json_writer.write_json(data=data, pathname=pathname, destination=destination)
