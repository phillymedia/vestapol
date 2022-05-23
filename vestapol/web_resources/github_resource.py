from vestapol.web_resources import base_resource


class GitHubResource(base_resource.BaseResource):
    base_url = "https://raw.githubusercontent.com/"

    def __init__(
        self,
        name: str,
        endpoint: str,
        version: str,
        response_format_tag: str,
        external_data_format_tag: str,
        response_filename: str,
    ):
        super().__init__(
            name,
            self.base_url,
            endpoint,
            version,
            response_format_tag,
            external_data_format_tag,
            response_filename,
        )
