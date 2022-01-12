from abc import abstractmethod
from vestapol.writers import json_writer
from vestapol.web_resources import base_resource


class JSONResource(base_resource.BaseResource):
    response_format_tag = 'json'
    external_data_format_tag = 'jsonl'
    response_filename = 'data.json'

    def __init__(self, name=None, base_url=None, endpoint=None, version=None):
        self.name = name or self.name
        self.base_url = base_url or self.base_url
        self.endpoint = endpoint or self.endpoint
        self.version = version or self.version
        super().__init__(self.name, self.base_url, self.endpoint, self.version, self.response_format_tag, self.external_data_format_tag, self.response_filename)


    def load(self, destination):
        data = self.extract_data()
        self.write_data(data, destination)
        self.unnest_data(data, destination)
        return data

    def write_data(self, api_data, destination):
        json_writer.write_json(
            api_data, self.response_target_prefix / self.response_filename, destination)

    @abstractmethod
    def unnest_data(self, data, destination):
        pass

    def write_list(self, data: list[dict], destination, data_path=None):
        pathname = self.get_pathname(data_path)
        json_writer.write_jsonl(
            data=data, pathname=pathname, destination=destination)

    def write_dict(self, data: dict, destination, data_path=None):
        pathname = self.get_pathname(data_path)
        json_writer.write_json(
            data=data, pathname=pathname, destination=destination)

    def get_pathname(self, data_path=None):
        jsonl_target_prefix = self.get_response_root(
            self.external_data_format_tag)

        if data_path:
            hive_path = self.get_hive_path(data_path)
            pathname = jsonl_target_prefix / hive_path / self.response_filename
        else:
            pathname = jsonl_target_prefix / self.response_filename

        return pathname
