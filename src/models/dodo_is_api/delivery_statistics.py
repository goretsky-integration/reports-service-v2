from uuid import UUID

from pydantic import BaseModel, Field, computed_field

__all__ = ('UnitDeliveryStatistics',)


class UnitDeliveryStatistics(BaseModel):
    unit_uuid: UUID = Field(alias='unitId')
    unit_name: str = Field(alias='unitName')
    delivery_sales: int = Field(alias='deliverySales')
    delivery_orders_count: int = Field(alias='deliveryOrdersCount')
    average_delivery_order_fulfillment_time_in_seconds: int = Field(
        alias='avgDeliveryOrderFulfillmentTime',
    )
    average_cooking_time_in_seconds: int = Field(alias='avgCookingTime')
    average_heated_shelf_time_in_seconds: int = Field(
        alias='avgHeatedShelfTime',
    )
    average_order_trip_time_in_seconds: int = Field(alias='avgOrderTripTime')
    late_orders_count: int = Field(alias='lateOrdersCount')
    trips_count: int = Field(alias='tripsCount')
    trips_duration_in_seconds: int = Field(alias='tripsDuration')
    couriers_shifts_duration_in_seconds: int = Field(
        alias='couriersShiftsDuration',
    )
    orders_with_courier_app_count: int = Field(
        alias='ordersWithCourierAppCount',
    )

    @computed_field
    def orders_per_labor_hour(self) -> int | float:
        if self.couriers_shifts_duration_in_seconds == 0:
            return 0

        value = self.delivery_orders_count / (
                self.couriers_shifts_duration_in_seconds / 3600)
        return round(value, 1)
