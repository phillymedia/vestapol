from vestapol.writers import text_writer, json_writer
from vestapol.web_resources import base_resource


class CSVResource(base_resource.BaseResource):
    header_format_tag = 'header'
    header_filename = 'header.json'
    response_format_tag = external_data_format_tag = 'csv'
    response_filename = 'data.csv'
    header_data: dict

    def __init__(self, name=None, base_url=None, endpoint=None, version=None, has_header=None):
        self.name = name or self.name
        self.base_url = base_url or self.base_url
        self.endpoint = endpoint or self.endpoint
        self.version = version or self.version
        super().__init__(self.name, self.base_url, self.endpoint, self.version, self.response_format_tag, self.external_data_format_tag, self.response_filename)
        
        self.has_header = has_header or self.has_header

    def load(self, destination):
        data = self.extract_data()
        self.write_data(data, destination)
        if self.has_header:
            self.write_header(data, destination)
        return data

    def write_data(self, data, destination):
        text_writer.write_text(
            data, self.response_target_prefix / self.response_filename, destination)

    def write_header(self, data, destination):
        header_row = data.split('\n')[0]
        self.header_data = {
            'column_metadata': [
                {
                    'name': column,
                    'index': idx
                } for idx, column in enumerate(header_row.split(','))
            ]
        }

        json_writer.write_json(
            self.header_data, self.get_response_root(self.header_format_tag) / self.header_filename, destination)
