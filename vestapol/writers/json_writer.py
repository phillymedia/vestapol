import json
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


def write_json(data: dict, pathname, destination):
    if not isinstance(data, dict):
        raise TypeError(f"Expected a dict, received {type(data)}")

    data_string = json.dumps(data)
    destination.write_data(data_string, pathname)


def write_jsonl(data: List[Dict], pathname, destination):
    if not isinstance(data, list):
        raise TypeError(f"Expected a list, received {type(data)}")
    
    data_string = "\n".join([json.dumps(record) for record in data])

    destination.write_data(data_string, pathname)
