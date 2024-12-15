from collections.abc import Iterable
from functools import cached_property
from uuid import UUID

from domain.production.models import (
    UnitSalesStatistics,
    TotalSalesStatistics,
    SalesStatistics,
)
from interactors.productivity_statistics import FetchResult
from models.dodo_is_api import UnitProductivityStatistics
from models.events import Event


def compute_growth_in_percents(
    current_value: int,
    previous_value: int,
) -> int:
    if previous_value == 0:
        return 0
    return int(100 - current_value * 100 / previous_value)


def map_unit_uuid_to_productivity_statistics(
    results: Iterable[FetchResult[list[UnitProductivityStatistics]]],
) -> dict[UUID, UnitProductivityStatistics]:
    unit_uuid_to_statistics: dict[UUID, UnitProductivityStatistics] = {}
    for result in results:
        if result.data is None:
            continue
        for unit_productivity_statistics in result.data:
            unit_uuid = unit_productivity_statistics.unit_uuid
            unit_uuid_to_statistics[unit_uuid] = unit_productivity_statistics
    return unit_uuid_to_statistics


class SalesStatisticsReportGenerator:
    def __init__(
        self,
        event: Event,
        productivity_statistics_fetch_results_for_today: Iterable[
            FetchResult[list[UnitProductivityStatistics]]
        ],
        productivity_statistics_fetch_results_for_week_before: Iterable[
            FetchResult[list[UnitProductivityStatistics]]
        ],
    ) -> None:
        self.__event = event
        self.__productivity_statistics_fetch_results_for_today = (
            productivity_statistics_fetch_results_for_today
        )
        self.__productivity_statistics_fetch_results_for_week_before = (
            productivity_statistics_fetch_results_for_week_before
        )

    def get_event_units_uuids_and_names(self) -> list[tuple[UUID, str]]:
        return [(unit.uuid, unit.name) for unit in self.__event.units]

    @cached_property
    def unit_uuid_to_statistics_for_today(
        self,
    ) -> dict[UUID, UnitProductivityStatistics]:
        return map_unit_uuid_to_productivity_statistics(
            results=self.__productivity_statistics_fetch_results_for_today,
        )

    @cached_property
    def unit_uuid_to_statistics_for_week_before(
        self,
    ) -> dict[UUID, UnitProductivityStatistics]:
        return map_unit_uuid_to_productivity_statistics(
            results=self.__productivity_statistics_fetch_results_for_week_before,
        )

    def get_total_sales_statistics(self) -> TotalSalesStatistics:
        units_sales_for_today = [
            unit_sales_statistics.sales
            for unit_sales_statistics in self.unit_uuid_to_statistics_for_today.values()
        ]
        units_sales_for_week_before = [
            unit_sales_statistics.sales
            for unit_sales_statistics in self.unit_uuid_to_statistics_for_week_before.values()
        ]

        total_sales_for_today = sum(units_sales_for_today)
        total_sales_for_week_before = sum(units_sales_for_week_before)

        growth_from_week_before = compute_growth_in_percents(
            current_value=total_sales_for_today,
            previous_value=total_sales_for_week_before,
        )

        return TotalSalesStatistics(
            sales_for_today=total_sales_for_today,
            sales_growth_from_week_before_in_percents=growth_from_week_before,
        )

    def get_unit_sales_statistics(
        self,
        *,
        unit_uuid: UUID,
        unit_name: str,
    ) -> UnitSalesStatistics:
        sales_for_today: int | None = None
        if unit_uuid in self.unit_uuid_to_statistics_for_today:
            productivity_statistics = self.unit_uuid_to_statistics_for_today[unit_uuid]
            sales_for_today = productivity_statistics.sales

        sales_for_week_before: int | None = None
        if unit_uuid in self.unit_uuid_to_statistics_for_week_before:
            productivity_statistics = self.unit_uuid_to_statistics_for_week_before[
                unit_uuid
            ]
            sales_for_week_before = productivity_statistics.sales

        growth_from_week_before: int | None = None
        if sales_for_today is not None and sales_for_week_before is not None:
            growth_from_week_before = compute_growth_in_percents(
                current_value=sales_for_today,
                previous_value=sales_for_week_before,
            )
        return UnitSalesStatistics(
            unit_name=unit_name,
            sales_for_today=sales_for_today,
            sales_growth_from_week_before_in_percents=growth_from_week_before,
        )

    def get_units_sales_statistics(self) -> list[UnitSalesStatistics]:
        unit_uuids_and_names = self.get_event_units_uuids_and_names()
        return [
            self.get_unit_sales_statistics(
                unit_uuid=unit_uuid,
                unit_name=unit_name,
            )
            for unit_uuid, unit_name in unit_uuids_and_names
        ]

    def get_report(self) -> SalesStatistics:
        return SalesStatistics(
            units=self.get_units_sales_statistics(),
            total=self.get_total_sales_statistics(),
        )
