from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from enums import LateDeliveryVoucherIssuer

__all__ = ('LateDeliveryVoucher',)


class LateDeliveryVoucher(BaseModel):
    order_id: UUID = Field(alias='orderId')
    order_number: str = Field(alias='orderNumber')
    order_accepted_at: datetime = Field(alias='orderAcceptedAtLocal')
    unit_uuid: UUID = Field(alias='unitId')
    predicted_delivery_time: datetime = Field(
        alias='predictedDeliveryTimeLocal',
    )
    order_fulfilment_flag_at: datetime | None = Field(
        alias='orderFulfilmentFlagAtLocal',
    )
    delivery_deadline: datetime = Field(alias='deliveryDeadlineLocal')
    issuer_name: LateDeliveryVoucherIssuer | None = Field(alias='issuerName')
    courier_staff_id: UUID | None = Field(alias='courierStaffId')
