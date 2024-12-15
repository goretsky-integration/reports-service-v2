import asyncio
from collections.abc import Iterable

from fast_depends import Depends, inject

from connections import (
    AuthCredentialsStorageConnection,
    DodoIsApiConnection,
)
from dependencies import (
    get_auth_credentials_storage_connection,
    get_dodo_is_api_connection,
)
from helpers import batched
from models import Event, LateDeliveryVoucher, Unit

from parsers import (
    group_by_dodo_is_api_account_name,
    parse_account_tokens_response,
)
from parsers.dodo_is_api import parse_late_delivery_vouchers_response
from services import compute_late_delivery_vouchers_statistics
from time_helpers import Period
from handlers.router import router


async def process_account_units_for_late_delivery_vouchers(
    account_name: str,
    units: Iterable[Unit],
    dodo_is_api_connection: DodoIsApiConnection,
    auth_credentials_storage_connection: AuthCredentialsStorageConnection,
) -> tuple[list[LateDeliveryVoucher], list[LateDeliveryVoucher]]:
    account_tokens = await auth_credentials_storage_connection.get_tokens(
        account_name=account_name,
    )
    account_tokens = parse_account_tokens_response(account_tokens)

    unit_uuids = [unit.uuid for unit in units]

    async with asyncio.TaskGroup() as task_group:
        period_today = Period.today_to_this_time()
        today_task = task_group.create_task(
            dodo_is_api_connection.get_late_delivery_vouchers(
                access_token=account_tokens.access_token,
                unit_uuids=unit_uuids,
                from_datetime=period_today.from_datetime,
                to_datetime=period_today.to_datetime,
            ),
        )

        period_week_before = Period.week_before_today_to_this_time()
        week_before_task = task_group.create_task(
            dodo_is_api_connection.get_late_delivery_vouchers(
                access_token=account_tokens.access_token,
                unit_uuids=unit_uuids,
                from_datetime=period_week_before.from_datetime,
                to_datetime=period_week_before.to_datetime,
            ),
        )

    return (
        parse_late_delivery_vouchers_response(today_task.result()),
        parse_late_delivery_vouchers_response(week_before_task.result()),
    )


def unpack_tasks(tasks: Iterable[asyncio.Task]) -> tuple[list, list]:
    all_vouchers_for_today = []
    all_vouchers_for_week_before = []

    for task in tasks:
        vouchers_for_today, vouchers_for_week_before = task.result()
        all_vouchers_for_today += vouchers_for_today
        all_vouchers_for_week_before += vouchers_for_week_before

    return all_vouchers_for_today, all_vouchers_for_week_before


@router.subscriber("late-delivery-vouchers")
@router.publisher("specific-chats-event")
@inject
async def on_late_delivery_vouchers_event(
    event: Event,
    auth_credentials_storage_connection: (AuthCredentialsStorageConnection) = Depends(
        get_auth_credentials_storage_connection,
        use_cache=False,
    ),
    dodo_is_api_connection: DodoIsApiConnection = Depends(
        get_dodo_is_api_connection,
        use_cache=False,
    ),
):
    account_name_to_units = group_by_dodo_is_api_account_name(event.units)

    tasks = []
    async with asyncio.TaskGroup() as task_group:
        for account_name, units_group in account_name_to_units.items():
            for units_group_batch in batched(units_group, batch_size=2):
                task = task_group.create_task(
                    process_account_units_for_late_delivery_vouchers(
                        account_name=account_name,
                        units=units_group_batch,
                        dodo_is_api_connection=dodo_is_api_connection,
                        auth_credentials_storage_connection=auth_credentials_storage_connection,
                    ),
                )
                tasks.append(task)

    vouchers_for_today, vouchers_for_week_before = unpack_tasks(tasks)

    unit_uuid_to_name = {unit.uuid: unit.name for unit in event.units}

    vouchers_statistics = compute_late_delivery_vouchers_statistics(
        vouchers_for_today=vouchers_for_today,
        vouchers_for_week_before=vouchers_for_week_before,
        unit_uuid_to_name=unit_uuid_to_name,
    )
    return {
        "type": "LATE_DELIVERY_VOUCHERS",
        "payload": vouchers_statistics,
        "chat_ids": event.chat_ids,
    }
