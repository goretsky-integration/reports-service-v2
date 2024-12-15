from dataclasses import dataclass


__all__ = ("UnitSalesStatistics",)


@dataclass(frozen=True, slots=True)
class UnitSalesStatistics:
    unit_name: str
    sales_for_today: int | None = None
    sales_growth_from_week_before_in_percents: int | None = None
    error_code: str | None = None
