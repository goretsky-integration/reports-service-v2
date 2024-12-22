import asyncio
from collections.abc import Iterable
from uuid import UUID

import httpx
from pydantic import SecretStr

from connections.dodo_is_api import DodoIsApiConnection
from models import (
    FetchResult,
    AccountTokensAndUnitUUIDs,
    UnitSales,
)
from helpers import batched
from time_helpers import Period
from enums import ErrorCode
from logger import create_logger
from parsers import parse_units_sales_for_period_response
from exceptions import ConnectionResponseParseError

__all__ = ("UnitsSalesFetchInteractor",)


logger = create_logger("interactors:units_sales")


class UnitsSalesFetchInteractor:
    def __init__(
        self,
        dodo_is_api_connection: DodoIsApiConnection,
        accounts_tokens_and_unit_uuids: Iterable[AccountTokensAndUnitUUIDs],
        period: Period,
    ) -> None:
        self.__dodo_is_api_connection = dodo_is_api_connection
        self.__accounts_tokens_and_unit_uuids = accounts_tokens_and_unit_uuids
        self.__period = period

    async def fetch_one(
        self,
        *,
        unit_uuids: Iterable[UUID],
        access_token: SecretStr,
    ) -> FetchResult[list[UnitSales]]:
        unit_uuids = tuple(unit_uuids)
        try:
            try:
                response = (
                    await self.__dodo_is_api_connection.get_units_sales_for_period(
                        unit_uuids=unit_uuids,
                        access_token=access_token,
                        from_datetime=self.__period.from_datetime,
                        to_datetime=self.__period.to_datetime,
                    )
                )
            except httpx.HTTPError as error:
                logger.error(
                    "Http error occurred while fetching units sales: %s",
                    str(error),
                )
                return FetchResult(
                    unit_uuids=unit_uuids,
                    exception=error,
                    error_code=ErrorCode.HTTP_ERROR,
                )
            try:
                units_sales = parse_units_sales_for_period_response(response)
            except ConnectionResponseParseError as error:
                return FetchResult(
                    unit_uuids=unit_uuids,
                    exception=error,
                    error_code=ErrorCode.PARSE_ERROR,
                )
            return FetchResult(unit_uuids=tuple(unit_uuids), data=units_sales)
        except Exception as error:
            logger.error(
                "Unexpected error occurred while fetching units sales: %s",
                str(error),
            )
            return FetchResult(
                unit_uuids=unit_uuids,
                exception=error,
                error_code=ErrorCode.UNEXPECTED_ERROR,
            )

    async def fetch_all(self) -> list[FetchResult[list[UnitSales]]]:
        units_count_per_request: int = 30

        tasks: list[asyncio.Task] = []
        async with asyncio.TaskGroup() as task_group:
            for account_tokens_and_unit_uuids in self.__accounts_tokens_and_unit_uuids:
                access_token = account_tokens_and_unit_uuids.access_token
                unit_uuids = account_tokens_and_unit_uuids.unit_uuids

                for unit_uuids_batch in batched(
                    unit_uuids,
                    batch_size=units_count_per_request,
                ):
                    task = task_group.create_task(
                        self.fetch_one(
                            unit_uuids=unit_uuids_batch,
                            access_token=access_token,
                        )
                    )
                    tasks.append(task)

        return [task.result() for task in tasks]
