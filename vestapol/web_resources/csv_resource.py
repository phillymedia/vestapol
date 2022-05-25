from __future__ import annotations

from typing import TYPE_CHECKING

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
        base_url: str,
        endpoint: str,
        version: str,
        has_header: bool,
        query_params: dict = None,
        request_headers: dict = None,
    ):
        self.name = name
        self.base_url = base_url
        self.endpoint = endpoint
        self.version = version
        self.has_header = has_header
        self.query_params = query_params
        self.request_headers = request_headers

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
        )

    def load(self, destination: DestinationTypes) -> str:
        data = self.request_data()
        self.write_data(data, destination)
        if self.has_header:
            self.write_header(data, destination)
        return data

    def write_data(self, data: str, destination: DestinationTypes):
        text_writer.write_text(
            data, self.response_target_prefix / self.response_filename, destination
        )

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
