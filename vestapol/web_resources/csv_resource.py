from __future__ import annotations

from typing import Dict, List, Tuple, Any, Optional, TYPE_CHECKING

from vestapol.web_resources import base_resource
from vestapol.writers import json_writer
from vestapol.writers import text_writer

if TYPE_CHECKING:
    from vestapol.destinations import DestinationTypes


class CSVResource(base_resource.BaseResource):
    header_format_tag = "header"
    header_filename = "header.json"
    response_format_tag = external_data_format_tag = "csv"
    response_filename = "data.csv"
    header_data: dict

    def __init__(
        self,
        name: str,
        base_url: Optional[str],
        endpoint: Optional[str],
        version: str,
        has_header: bool,
        query_params: dict = None,
        request_headers: dict = None,
        manual_schema: List[Dict] = None,
    ):
        self.name = name
        self.base_url = base_url
        self.endpoint = endpoint
        self.version = version
        self.has_header = has_header
        self.query_params = query_params
        self.request_headers = request_headers
        self.manual_schema = manual_schema

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

    def load(self, destination: DestinationTypes) -> str:
        data = self.request_data()
        self.write_data(data, destination)
        if self.has_header:
            self.write_header(data, destination)
        return data

    def write_data(self, data, destination: DestinationTypes):
        self.write_string(data, destination, data_path=None)

    def write_string(
        self,
        data: str,
        destination: DestinationTypes,
        data_path: List[Tuple[str, Any]] = None,
    ):
        pathname = self.get_pathname(data_path)
        text_writer.write_text(data, pathname, destination)

    def write_header(self, data: str, destination: DestinationTypes):
        header_row = data.split("\n")[0]
        self.header_data = {
            "columns": [
                {"name": column, "index": idx}
                for idx, column in enumerate(header_row.split(","))
            ]
        }

        json_writer.write_json(
            self.header_data,
            self.get_response_root(self.header_format_tag) / self.header_filename,
            destination,
        )
