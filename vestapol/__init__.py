from vestapol import web_resources
from vestapol import destinations

import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass
