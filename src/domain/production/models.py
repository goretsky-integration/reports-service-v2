from dataclasses import dataclass


__all__ = ("UnitSalesStatistics", "TotalSalesStatistics", "SalesStatistics")


@dataclass(frozen=True, slots=True)
class UnitSalesStatistics:
    unit_name: str
    sales_for_today: int | None = None
    sales_growth_from_week_before_in_percents: int | None = None
    error_code: str | None = None


@dataclass(frozen=True, slots=True)
class TotalSalesStatistics:
    sales_for_today: int
    sales_growth_from_week_before_in_percents: int


@dataclass(frozen=True, slots=True)
class SalesStatistics:
    units: list[UnitSalesStatistics]
    total: TotalSalesStatistics
