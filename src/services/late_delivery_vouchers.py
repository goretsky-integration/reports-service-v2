from collections.abc import Iterable
from typing import TypeAlias
from uuid import UUID

from models import LateDeliveryVoucher, UnitLateDeliveryVouchers
from parsers import group_by_unit_uuid

__all__ = ('compute_late_delivery_vouchers_statistics',)

LateDeliveryVouchers: TypeAlias = Iterable[LateDeliveryVoucher]


def compute_late_delivery_vouchers_statistics(
        vouchers_for_today: LateDeliveryVouchers,
        vouchers_for_week_before: LateDeliveryVouchers,
        unit_uuid_to_name: dict[UUID, str],
) -> list[UnitLateDeliveryVouchers]:
    vouchers_for_today_grouped_by_unit_uuid = (
        group_by_unit_uuid(vouchers_for_today)
    )
    vouchers_for_week_before_grouped_by_unit_uuid = (
        group_by_unit_uuid(vouchers_for_week_before)
    )

    units_late_delivery_vouchers: list[UnitLateDeliveryVouchers] = []
    for unit_uuid, unit_name in unit_uuid_to_name.items():
        unit_vouchers_for_today = (
            vouchers_for_today_grouped_by_unit_uuid.get(unit_uuid, [])
        )
        unit_vouchers_for_week_before = (
            vouchers_for_week_before_grouped_by_unit_uuid.get(unit_uuid, [])
        )
        unit_vouchers_for_today_count = len(unit_vouchers_for_today)
        unit_vouchers_for_week_before_count = len(unit_vouchers_for_week_before)

        unit_late_delivery_vouchers = UnitLateDeliveryVouchers(
            unit_name=unit_name,
            certificates_count_today=unit_vouchers_for_today_count,
            certificates_count_week_before=unit_vouchers_for_week_before_count,
        )
        units_late_delivery_vouchers.append(unit_late_delivery_vouchers)

    return units_late_delivery_vouchers
