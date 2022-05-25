from typing import Union

from vestapol.web_resources.csv_resource import CSVResource
from vestapol.web_resources.github_resource import GitHubResource
from vestapol.web_resources.json_resource import JSONResource

ResourceTypes = Union[CSVResource, GitHubResource, JSONResource]
