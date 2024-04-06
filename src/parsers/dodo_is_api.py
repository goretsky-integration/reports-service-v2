import httpx
from pydantic import TypeAdapter

from models import LateDeliveryVoucher

__all__ = ('parse_late_delivery_vouchers_response',)


def parse_late_delivery_vouchers_response(
        response: httpx.Response,
) -> list[LateDeliveryVoucher]:
    type_adapter = TypeAdapter(list[LateDeliveryVoucher])
    response_data = response.json()
    return type_adapter.validate_python(response_data['vouchers'])
