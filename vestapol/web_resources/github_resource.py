from vestapol.web_resources import base_resource


class GitHubResource(base_resource.BaseResource):
    base_url = "https://raw.githubusercontent.com/"

    def __init__(
        self,
        name,
        endpoint,
        version,
        response_format_tag,
        external_data_format_tag,
        response_filename,
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
