from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from enums import LateDeliveryVoucherIssuer

__all__ = ("LateDeliveryVoucher", "UnitProductivityStatistics")


class LateDeliveryVoucher(BaseModel):
    order_id: UUID = Field(alias="orderId")
    order_number: str = Field(alias="orderNumber")
    order_accepted_at: datetime = Field(alias="orderAcceptedAtLocal")
    unit_uuid: UUID = Field(alias="unitId")
    predicted_delivery_time: datetime = Field(
        alias="predictedDeliveryTimeLocal"
    )
    order_fulfilment_flag_at: datetime | None = Field(
        alias="orderFulfilmentFlagAtLocal"
    )
    delivery_deadline: datetime = Field(alias="deliveryDeadlineLocal")
    issuer_name: LateDeliveryVoucherIssuer | None = Field(alias="issuerName")
    courier_staff_id: UUID | None = Field(alias="courierStaffId")


class UnitProductivityStatistics(BaseModel):
    unit_uuid: UUID = Field(validation_alias="unitId")
    unit_name: str = Field(validation_alias="unitName")
    labor_hours: float = Field(validation_alias="laborHours")
    sales: int
    sales_per_labor_hour: float = Field(validation_alias="salesPerLaborHour")
    products_per_labor_hour: float = Field(
        validation_alias="productsPerLaborHour",
    )
    average_heated_shelf_time_in_seconds: int = Field(
        validation_alias="avgHeatedShelfTime",
    )
    orders_per_courier_labour_hour: float = Field(
        validation_alias="ordersPerCourierLabourHour",
    )
