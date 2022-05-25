from typing import Union

from vestapol.destinations.gcp_destination import GoogleCloudPlatform
from vestapol.destinations.local_destination import Local

DestinationTypes = Union[GoogleCloudPlatform, Local]
