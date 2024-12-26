from fast_depends import Depends

from handlers.router import router
from application.enums import QueueName
from models.events import Event
from dependencies.dodo_is_api import (
    DodoIsApiConnection,
    get_dodo_is_api_connection,
)
from dependencies.auth_credentials_storage import (
    AuthCredentialsStorageConnection,
    get_auth_credentials_storage_connection,
)
from interactors import (
    StaffMembersBirthdaysFetchInteractor,
    AuthTokensFetchInteractor,
)
from logger import create_logger
from time_helpers import Period
from parsers import (
    to_dodo_is_api_account_names,
    merge_account_tokens_and_units,
)

logger = create_logger("handlers:staff_members_birthdays")


@router.subscriber(QueueName.STAFF_MEMBERS_BIRTHDAYS)
async def on_staff_members_birthdays_event(
    event: Event,
    dodo_is_api_connection: DodoIsApiConnection = Depends(
        get_dodo_is_api_connection,
        use_cache=False,
    ),
    auth_credentials_storage_connection: (AuthCredentialsStorageConnection) = Depends(
        get_auth_credentials_storage_connection,
        use_cache=False,
    ),
):
    account_names = to_dodo_is_api_account_names(event.units)
    auth_tokens_fetch_interactor = AuthTokensFetchInteractor(
        account_names=account_names,
        auth_credentials_storage_connection=auth_credentials_storage_connection,
    )
    auth_tokens_fetch_results = await auth_tokens_fetch_interactor.fetch_all()

    logger.info("Fetched auth tokens: %s", auth_tokens_fetch_results)

    accounts_tokens = [
        auth_tokens_fetch_result.data
        for auth_tokens_fetch_result in auth_tokens_fetch_results
        if auth_tokens_fetch_result.data is not None
    ]

    accounts_tokens_and_unit_uuids = merge_account_tokens_and_units(
        units=event.units,
        accounts_tokens=accounts_tokens,
    )

    period = Period.today_to_this_time()

    birthdays_fetch_interactor = StaffMembersBirthdaysFetchInteractor(
        dodo_is_api_connection=dodo_is_api_connection,
        accounts_tokens_and_unit_uuids=accounts_tokens_and_unit_uuids,
        period=period,
    )

    birthdays_fetch_results = await birthdays_fetch_interactor.fetch_all()

    logger.debug(
        "Fetched staff members birthdays: %s",
        birthdays_fetch_results,
    )
