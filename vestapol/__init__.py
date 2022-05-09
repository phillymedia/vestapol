import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s %(name)s %(levelname)s:%(message)s"
)

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass
