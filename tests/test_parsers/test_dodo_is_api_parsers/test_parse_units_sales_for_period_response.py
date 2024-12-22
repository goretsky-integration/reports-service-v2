import json

import pytest
import httpx

from exceptions.parsers import ConnectionResponseParseError
from parsers.dodo_is_api import parse_units_sales_for_period_response


def test_parse_units_sales_for_period_response_success():
    data = {
        "result": [
            {"unitId": "e19cc4af-93f6-43c3-a699-bc0b029b7440", "sales": 100},
            {"unitId": "629937bb-212c-4f91-9ded-36d001831381", "sales": 200},
        ]
    }
    response = httpx.Response(200, content=json.dumps(data))

    result = parse_units_sales_for_period_response(response)
    assert len(result) == 2


def test_parse_units_sales_for_period_response_key_error():
    data = {
        "unitsSales": [
            {"unitId": "e19cc4af-93f6-43c3-a699-bc0b029b7440", "sales": 100},
            {"unitId": "629937bb-212c-4f91-9ded-36d001831381", "sales": 200},
        ]
    }
    response = httpx.Response(200, content=json.dumps(data))

    with pytest.raises(ConnectionResponseParseError) as excinfo:
        parse_units_sales_for_period_response(response)
    assert "Could not find 'result' key in response data" in str(excinfo.value)


def test_parse_units_sales_for_period_response_validation_error():
    data = {
        "result": [
            {"unitId": 4432, "sales": 100},
            {"unitId": 234, "sales": 200},
        ]
    }
    response = httpx.Response(200, content=json.dumps(data))

    with pytest.raises(ConnectionResponseParseError) as excinfo:
        parse_units_sales_for_period_response(response)
    assert "Pydantic validation error" in str(excinfo.value)
