from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import TYPE_CHECKING

from vestapol.web_resources import base_resource
from vestapol.writers import text_writer

if TYPE_CHECKING:
    from vestapol.destinations.base_destination import BaseDestination


class CSVResource(base_resource.BaseResource):
    response_format_tag = external_data_format_tag = "csv"
    response_filename = "data.csv"

    def __init__(
        self,
        name: str,
        base_url: Optional[str],
        endpoint: Optional[str],
        version: str,
        skip_leading_rows: int = 0,
        query_params: dict = None,
        request_headers: dict = None,
        manual_schema: List[Dict] = None,
    ):
        self.name = name
        self.base_url = base_url
        self.endpoint = endpoint
        self.version = version
        self.skip_leading_rows = skip_leading_rows
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
            self.skip_leading_rows,
        )

    def write_data(self, data, destination: BaseDestination):
        self.write_string(data, destination, data_path=None)

    def write_string(
        self,
        data: str,
        destination: BaseDestination,
        data_path: List[Tuple[str, Any]] = None,
    ):
        pathname = self.get_pathname(data_path)
        text_writer.write_text(data, pathname, destination)
