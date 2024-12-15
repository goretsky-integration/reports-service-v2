from fast_depends import inject, Depends

from models.events import Event, SpecificChatsEvent
from dependencies.dodo_is_api import (
    DodoIsApiConnection,
    get_dodo_is_api_connection,
)
from dependencies.auth_credentials_storage import (
    AuthCredentialsStorageConnection,
    get_auth_credentials_storage_connection,
)
from interactors import (
    AuthTokensFetchInteractor,
    ProductivityStatisticsFetchInteractor,
)
from logger import create_logger
from parsers.units import to_uuids
from time_helpers import Period
from parsers import group_by_dodo_is_api_account_name
from domain.production.services import SalesStatisticsReportGenerator
from domain.production.models import SalesStatistics
from handlers.router import router

logger = create_logger("handlers:revenue")


@router.subscriber("sales-statistics")
@router.publisher("specific-chats-event")
@inject
async def on_revenue_report_event(
    event: Event,
    dodo_is_api_connection: DodoIsApiConnection = Depends(
        get_dodo_is_api_connection,
        use_cache=False,
    ),
    auth_credentials_storage_connection: (AuthCredentialsStorageConnection) = Depends(
        get_auth_credentials_storage_connection,
        use_cache=False,
    ),
) -> SpecificChatsEvent[SalesStatistics]:
    account_names = {unit.dodo_is_api_account_name for unit in event.units}
    auth_tokens_fetch_interactor = AuthTokensFetchInteractor(
        account_names=account_names,
        auth_credentials_storage_connection=auth_credentials_storage_connection,
    )
    auth_tokens_fetch_results = await auth_tokens_fetch_interactor.fetch_all()

    logger.info("Fetched auth tokens: %s", auth_tokens_fetch_results)

    account_name_to_access_token = {
        result.data.account_name: result.data.access_token
        for result in auth_tokens_fetch_results
        if result.data is not None
    }
    account_name_to_units = group_by_dodo_is_api_account_name(event.units)

    unit_uuids_and_access_tokens = [
        (
            to_uuids(account_name_to_units[account_name]),
            access_token,
        )
        for account_name, access_token in account_name_to_access_token.items()
    ]

    period = Period.today_to_this_time().rounded_to_upper_hour()
    producitivity_statistics_fetch_interactor = ProductivityStatisticsFetchInteractor(
        dodo_is_api_connection=dodo_is_api_connection,
        unit_uuids_and_access_tokens=unit_uuids_and_access_tokens,
        period=period,
    )
    productivity_statistics_fetch_results_for_today = (
        await producitivity_statistics_fetch_interactor.fetch_all()
    )
    logger.info(
        "Fetched productivity statistics for today: %s",
        productivity_statistics_fetch_results_for_today,
    )

    period = Period.week_before_today_to_this_time().rounded_to_upper_hour()
    producitivity_statistics_fetch_interactor = ProductivityStatisticsFetchInteractor(
        dodo_is_api_connection=dodo_is_api_connection,
        unit_uuids_and_access_tokens=unit_uuids_and_access_tokens,
        period=period,
    )
    productivity_statistics_fetch_results_for_week_before = (
        await producitivity_statistics_fetch_interactor.fetch_all()
    )
    logger.info(
        "Fetched productivity statistics for week before: %s",
        productivity_statistics_fetch_results_for_today,
    )

    report_generator = SalesStatisticsReportGenerator(
        event=event,
        productivity_statistics_fetch_results_for_today=productivity_statistics_fetch_results_for_today,
        productivity_statistics_fetch_results_for_week_before=productivity_statistics_fetch_results_for_week_before,
    )

    sales_statistics = report_generator.get_report()

    logger.info("Sales statistics report: %s", sales_statistics)

    return SpecificChatsEvent[SalesStatistics](
        type="SALES_STATISTICS",
        chat_ids=event.chat_ids,
        payload=sales_statistics,
    )
