import json
from typing import Any

import httpx

from exceptions import ConnectionResponseParseError


__all__ = ("parse_response_json_data",)


def parse_response_json_data(response: httpx.Response) -> Any:
    """
    Parse JSON data from the httpx.Response.

    Args:
        response (httpx.Response): The response object.

    Returns:
        The parsed JSON data.

    Raises:
        ConnectionResponseParseError: If the JSON data could not be decoded.
    """
    try:
        return response.json()
    except json.JSONDecodeError as error:
        raise ConnectionResponseParseError(
            "Could not decode JSON response",
            response=response,
        ) from error
