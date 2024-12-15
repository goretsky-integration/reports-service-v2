import asyncio
from collections.abc import Iterable
from typing import Generic, TypeVar
from dataclasses import dataclass
from uuid import UUID

import httpx
from pydantic import SecretStr

from connections.dodo_is_api import DodoIsApiConnection
from models import UnitProductivityStatistics
from helpers import batched
from time_helpers import Period
from enums import ErrorCode
from logger import create_logger
from parsers import parse_productivity_statistics_response
from exceptions import ConnectionResponseParseError

__all__ = ("FetchResult", "ProductivityStatisticsFetchInteractor")

T = TypeVar("T")

logger = create_logger("interactors:productivity_statistics_fetcher")


@dataclass(frozen=True, slots=True)
class FetchResult(Generic[T]):
    unit_uuids: tuple[UUID, ...]
    data: T | None = None
    exception: Exception | None = None
    error_code: str | None = None


class ProductivityStatisticsFetchInteractor:
    def __init__(
        self,
        dodo_is_api_connection: DodoIsApiConnection,
        unit_uuids_and_access_tokens: Iterable[
            tuple[Iterable[UUID], SecretStr]
        ],
        period: Period,
    ) -> None:
        self.__dodo_is_api_connection = dodo_is_api_connection
        self.__unit_uuids_and_access_tokens = tuple(
            unit_uuids_and_access_tokens
        )
        self.__period = period

    async def fetch_one(
        self,
        *,
        unit_uuids: Iterable[UUID],
        access_token: SecretStr,
    ) -> FetchResult[list[UnitProductivityStatistics]]:
        unit_uuids = tuple(unit_uuids)
        try:
            try:
                response = await self.__dodo_is_api_connection.get_productivity_statistics(
                    unit_uuids=unit_uuids,
                    access_token=access_token,
                    from_datetime=self.__period.from_datetime,
                    to_datetime=self.__period.to_datetime,
                )
            except httpx.HTTPError as error:
                logger.error(
                    "Http error occurred while fetching productivity statistics: %s",
                    str(error),
                )
                return FetchResult(
                    unit_uuids=unit_uuids,
                    exception=error,
                    error_code=ErrorCode.HTTP_ERROR,
                )
            try:
                productivity_statistics = (
                    parse_productivity_statistics_response(response)
                )
            except ConnectionResponseParseError as error:
                return FetchResult(
                    unit_uuids=unit_uuids,
                    exception=error,
                    error_code=ErrorCode.PARSE_ERROR,
                )
            return FetchResult(unit_uuids=tuple(unit_uuids), data=productivity_statistics)
        except Exception as error:
            logger.error(
                "Unexpected error occurred while fetching productivity statistics: %s",
                str(error),
            )
            return FetchResult(
                unit_uuids=unit_uuids,
                exception=error,
                error_code=ErrorCode.UNEXPECTED_ERROR,
            )

    async def fetch_all(self):
        units_count_per_request: int = 30

        tasks: list[asyncio.Task] = []
        async with asyncio.TaskGroup() as task_group:
            for unit_uuids, access_token in self.__unit_uuids_and_access_tokens:
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
