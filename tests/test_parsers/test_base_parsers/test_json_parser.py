import pytest
import httpx

from exceptions import ConnectionResponseParseError
from parsers.base import parse_response_json_data


def test_parse_response_json_data_dict():
    """
    Test parsing a valid JSON dictionary response.
    """
    test_data = '{"key": "value"}'
    response = httpx.Response(200, content=test_data)

    result = parse_response_json_data(response)

    assert result == {"key": "value"}
    assert isinstance(result, dict)


def test_parse_response_json_data_list():
    """
    Test parsing a valid JSON list response.
    """
    test_data = "[1, 2, 3]"
    response = httpx.Response(200, content=test_data)

    result = parse_response_json_data(response)

    assert result == [1, 2, 3]
    assert isinstance(result, list)


def test_parse_response_json_data_invalid_json():
    """
    Test that ConnectionResponseParseError is raised for invalid JSON.
    """
    response = httpx.Response(200, content='{"invalid": json')

    with pytest.raises(ConnectionResponseParseError) as exc_info:
        parse_response_json_data(response)

    # Optional: Check the error message and that the original response is attached
    error = exc_info.value
    assert str(error) == "Could not decode JSON response"
    assert hasattr(error, "response")
    assert error.response.status_code == 200


def test_parse_response_json_data_empty_string():
    """
    Test parsing an empty string JSON response.
    """
    response = httpx.Response(200, content='""')

    result = parse_response_json_data(response)

    assert result == ""


def test_parse_response_json_data_null():
    """
    Test parsing a null JSON response.
    """
    response = httpx.Response(200, content="null")

    result = parse_response_json_data(response)

    assert result is None


def test_parse_response_json_data_nested_structure():
    """
    Test parsing a nested JSON structure.
    """
    test_data = '{"users": [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]}'
    response = httpx.Response(200, content=test_data)

    result: dict = parse_response_json_data(response)

    assert result == {"users": [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]}
    assert len(result["users"]) == 2
