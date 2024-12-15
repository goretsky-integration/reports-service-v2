import httpx
from pydantic import TypeAdapter, ValidationError

from exceptions import ConnectionResponseParseError
from models import LateDeliveryVoucher, UnitProductivityStatistics
from parsers.base import parse_response_json_data

__all__ = (
    "parse_late_delivery_vouchers_response",
    "parse_productivity_statistics_response",
)


def parse_late_delivery_vouchers_response(
    response: httpx.Response,
) -> list[LateDeliveryVoucher]:
    type_adapter = TypeAdapter(list[LateDeliveryVoucher])
    response_data = response.json()
    return type_adapter.validate_python(response_data["vouchers"])


def parse_productivity_statistics_response(
    response: httpx.Response,
) -> list[UnitProductivityStatistics]:
    type_adapter = TypeAdapter(list[UnitProductivityStatistics])
    response_data: dict = parse_response_json_data(response)

    try:
        units_productivity_statistics = response_data["productivityStatistics"]
    except KeyError as error:
        raise ConnectionResponseParseError(
            "Could not find 'productivityStatistics' key in response data",
            response=response,
        ) from error
    try:
        return type_adapter.validate_python(units_productivity_statistics)
    except ValidationError as error:
        raise ConnectionResponseParseError(
            "Pydantic validation error",
            response=response,
        ) from error
