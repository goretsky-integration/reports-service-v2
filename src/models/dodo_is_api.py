from datetime import datetime, date
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field

from enums import LateDeliveryVoucherIssuer, StaffType

__all__ = (
    "LateDeliveryVoucher",
    "UnitProductivityStatistics",
    "UnitSales",
    "StaffMemberBirthday",
    "StaffMembersBirthdaysResponse",
)


class LateDeliveryVoucher(BaseModel):
    order_id: UUID = Field(alias="orderId")
    order_number: str = Field(alias="orderNumber")
    order_accepted_at: datetime = Field(alias="orderAcceptedAtLocal")
    unit_uuid: UUID = Field(alias="unitId")
    predicted_delivery_time: datetime = Field(alias="predictedDeliveryTimeLocal")
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


class UnitSales(BaseModel):
    unit_uuid: Annotated[UUID, Field(validation_alias="unitId")]
    sales: int


class StaffMemberBirthday(BaseModel):
    staff_id: Annotated[UUID, Field(validation_alias="staffId")]
    first_name: Annotated[str, Field(validation_alias="firstName")]
    last_name: Annotated[str, Field(validation_alias="lastName")]
    patronymic_name: Annotated[str | None, Field(validation_alias="patronymicName")]
    date_of_birth: Annotated[date, Field(validation_alias="dateOfBirth")]
    unit_uuid: Annotated[UUID, Field(validation_alias="unitId")]
    unit_name: Annotated[str, Field(validation_alias="unitName")]
    staff_type: Annotated[StaffType, Field(validation_alias="staffType")]
    position_id: Annotated[UUID | None, Field(validation_alias="positionId")]
    position_name: Annotated[str | None, Field(validation_alias="positionName")]


class StaffMembersBirthdaysResponse(BaseModel):
    birthdays: Annotated[tuple[StaffMemberBirthday, ...], Field(alias="Birthdays")]
    is_end_of_list_reached: Annotated[bool, Field(alias="IsEndOfListReached")]
