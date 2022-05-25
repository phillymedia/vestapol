from vestapol.destinations.gcp_destination import GoogleCloudPlatform
from vestapol.destinations.local_destination import Local
from typing import Union

DestinationTypes = Union[GoogleCloudPlatform, Local]
