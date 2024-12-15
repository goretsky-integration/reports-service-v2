import json
import uuid
import pytest
import httpx

from exceptions import ConnectionResponseParseError
from models import UnitProductivityStatistics
from parsers.dodo_is_api import parse_productivity_statistics_response


def test_parse_productivity_statistics_success():
    """
    Test successful parsing of productivity statistics.
    """
    test_unit_id = str(uuid.uuid4())
    test_data = {
        "productivityStatistics": [
            {
                "unitId": test_unit_id,
                "unitName": "Test Unit 1",
                "laborHours": 8.5,
                "sales": 1000,
                "salesPerLaborHour": 117.65,
                "productsPerLaborHour": 45.3,
                "avgHeatedShelfTime": 600,
                "ordersPerCourierLabourHour": 12.5,
            },
            {
                "unitId": str(uuid.uuid4()),
                "unitName": "Test Unit 2",
                "laborHours": 7.2,
                "sales": 950,
                "salesPerLaborHour": 131.94,
                "productsPerLaborHour": 48.6,
                "avgHeatedShelfTime": 450,
                "ordersPerCourierLabourHour": 14.2,
            },
        ]
    }

    response = httpx.Response(200, content=json.dumps(test_data))

    result = parse_productivity_statistics_response(response)

    assert len(result) == 2
    assert all(isinstance(item, UnitProductivityStatistics) for item in result)

    # Verify first item's details
    first_item = result[0]
    assert first_item.unit_uuid == uuid.UUID(test_unit_id)
    assert first_item.unit_name == "Test Unit 1"
    assert first_item.labor_hours == 8.5
    assert first_item.sales == 1000
    assert first_item.sales_per_labor_hour == 117.65
    assert first_item.products_per_labor_hour == 45.3
    assert first_item.average_heated_shelf_time_in_seconds == 600
    assert first_item.orders_per_courier_labour_hour == 12.5


def test_parse_productivity_statistics_missing_key():
    """
    Test raising ConnectionResponseParseError when 'productivityStatistics' key is missing.
    """
    test_data = {
        "other_key": [{"unitId": str(uuid.uuid4()), "unitName": "Test Unit"}]
    }

    response = httpx.Response(200, content=json.dumps(test_data))

    with pytest.raises(ConnectionResponseParseError) as exc_info:
        parse_productivity_statistics_response(response)

    error = exc_info.value
    assert (
        str(error)
        == "Could not find 'productivityStatistics' key in response data"
    )
    assert error.response == response


def test_parse_productivity_statistics_validation_error():
    """
    Test raising ConnectionResponseParseError when Pydantic validation fails.
    """
    test_data = {
        "productivityStatistics": [
            {
                # Missing required fields or incorrect types
                "unitId": "invalid-uuid",
                "unitName": 123,  # Should be a string
                "laborHours": "not a number",
                "sales": "invalid",
                "salesPerLaborHour": None,
                "productsPerLaborHour": {},
                "avgHeatedShelfTime": "too long",
                "ordersPerCourierLabourHour": [],
            }
        ]
    }

    response = httpx.Response(200, content=json.dumps(test_data))

    with pytest.raises(ConnectionResponseParseError) as exc_info:
        parse_productivity_statistics_response(response)

    error = exc_info.value
    assert str(error) == "Pydantic validation error"
    assert error.response == response


def test_parse_productivity_statistics_empty_list():
    """
    Test handling of an empty productivityStatistics list.
    """
    test_data = {"productivityStatistics": []}

    response = httpx.Response(200, content=json.dumps(test_data))

    result = parse_productivity_statistics_response(response)

    assert len(result) == 0


def test_parse_productivity_statistics_invalid_json():
    """
    Test handling of invalid JSON (this would be caught by parse_response_json_data).
    """
    response = httpx.Response(200, content='{"invalid": json')

    with pytest.raises(ConnectionResponseParseError):
        parse_productivity_statistics_response(response)
