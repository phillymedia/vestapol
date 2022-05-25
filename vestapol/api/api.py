import logging

import requests

logger = logging.getLogger(__name__)

JSON_FORMAT_TAG = "json"
CSV_FORMAT_TAG = "csv"


def get_api_data(
    url: str, response_format_tag: str, query_params: dict, request_headers: dict
):
    logger.debug(f"GET {url}")

    try:
        response = requests.get(url, params=query_params, headers=request_headers)
        logger.debug(response.url)
        response.raise_for_status()
    except Exception as e:
        logger.error(e)
        raise

    if response_format_tag == JSON_FORMAT_TAG:
        return response.json()

    elif response_format_tag == CSV_FORMAT_TAG:
        return response.text

    else:
        logger.error(f"Unsupported format tag: {response_format_tag}")
        raise ValueError(f"Unsupported format tag: {response_format_tag}")
