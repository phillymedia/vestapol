from vestapol.writers import text_writer, json_writer
from vestapol.web_resources import base_resource


class CSVResource(base_resource.BaseResource):
    response_format_tag = external_data_format_tag = 'csv'
    response_filename = 'data.csv'
    header_format_tag = 'header'
    header_filename = 'header.json'
    has_header: bool
    header_data: dict

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
