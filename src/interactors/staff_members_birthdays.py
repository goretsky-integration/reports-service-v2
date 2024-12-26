import asyncio
from uuid import UUID
from collections.abc import Iterable

from pydantic import SecretStr

from models import FetchResult, AccountTokensAndUnitUUIDs
from connections import DodoIsApiConnection
from models.dodo_is_api import StaffMemberBirthday
from parsers import parse_staff_members_birthdays_response
from time_helpers import Period
from helpers import batched


class StaffMembersBirthdaysFetchInteractor:
    def __init__(
        self,
        dodo_is_api_connection: DodoIsApiConnection,
        accounts_tokens_and_unit_uuids: Iterable[AccountTokensAndUnitUUIDs],
        period: Period,
    ) -> None:
        self.__connection = dodo_is_api_connection
        self.__accounts_tokens_and_unit_uuids = accounts_tokens_and_unit_uuids
        self.__period = period

    async def fetch_one(
        self,
        *,
        unit_uuids: Iterable[UUID],
        access_token: SecretStr,
    ):
        unit_uuids = tuple(unit_uuids)

        staff_members_birthdays: list[StaffMemberBirthday] = []

        take: int = 1000
        skip: int = 0
        while True:
            response = await self.__connection.get_staff_members_birthdays(
                access_token=access_token,
                unit_uuids=unit_uuids,
                day_from=self.__period.from_datetime.day,
                day_to=self.__period.to_datetime.day,
                month_from=self.__period.from_datetime.month,
                month_to=self.__period.to_datetime.month,
                take=take,
                skip=skip,
            )

            birthdays_response = parse_staff_members_birthdays_response(response)

            staff_members_birthdays += birthdays_response.birthdays

            if birthdays_response.is_end_of_list_reached:
                break

            skip += take

        return FetchResult[list[StaffMemberBirthday]](
            unit_uuids=unit_uuids,
            data=staff_members_birthdays,
        )

    async def fetch_all(self) -> list[FetchResult[list[StaffMemberBirthday]]]:
        units_count_per_request: int = 30

        tasks: list[asyncio.Task[FetchResult[list[StaffMemberBirthday]]]] = []
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
