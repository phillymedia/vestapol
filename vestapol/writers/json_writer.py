import json
import logging
from typing import Dict
from typing import List
from typing import Generator
from typing import Union

from vestapol.destinations.base_destination import BaseDestination

logger = logging.getLogger(__name__)


def write_json(data: dict, pathname: str, destination: BaseDestination):
    data_string = json.dumps(data)
    destination.write_data(data_string, pathname)


def write_jsonl(data: Union[List[Dict], Generator], pathname: str, destination: BaseDestination):
    data_string = "\n".join([json.dumps(record) for record in data])
    destination.write_data(data_string, pathname)
