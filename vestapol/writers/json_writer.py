import json
import logging
from typing import Dict
from typing import List

from vestapol.destinations import DestinationTypes

logger = logging.getLogger(__name__)


def write_json(data: dict, pathname: str, destination: DestinationTypes):
    data_string = json.dumps(data)
    destination.write_data(data_string, pathname)


def write_jsonl(data: List[Dict], pathname: str, destination: DestinationTypes):
    data_string = "\n".join([json.dumps(record) for record in data])
    destination.write_data(data_string, pathname)
