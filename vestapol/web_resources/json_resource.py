from abc import abstractmethod
from vestapol.writers import json_writer
from vestapol.web_resources import base_resource


class JSONResource(base_resource.BaseResource):
    response_format_tag = "json"
    external_data_format_tag = "jsonl"
    response_filename = "data.json"

    def __init__(self, name, base_url, endpoint, version):
        self.name = name
        self.base_url = base_url
        self.endpoint = endpoint
        self.version = version
        super().__init__(
            self.name,
            self.base_url,
            self.endpoint,
            self.version,
            self.response_format_tag,
            self.external_data_format_tag,
            self.response_filename,
        )

    def load(self, destination):
        data = self.request_data()
        self.write_data(data, destination)
        self.unnest_data(data, destination)
        return data

    def write_data(self, api_data, destination):
        json_writer.write_json(
            api_data, self.response_target_prefix / self.response_filename, destination
        )

    @abstractmethod
    def unnest_data(self, data, destination):
        pass

    def write_list(self, data: list[dict], destination, data_path=None):
        pathname = self.get_pathname(data_path)
        json_writer.write_jsonl(data=data, pathname=pathname, destination=destination)

    def write_dict(self, data: dict, destination, data_path=None):
        pathname = self.get_pathname(data_path)
        json_writer.write_json(data=data, pathname=pathname, destination=destination)

    def get_pathname(self, data_path=None):
        jsonl_target_prefix = self.get_response_root(self.external_data_format_tag)

        if data_path:
            hive_path = self.get_hive_path(data_path)
            pathname = jsonl_target_prefix / hive_path / self.response_filename
        else:
            pathname = jsonl_target_prefix / self.response_filename

        return pathname
