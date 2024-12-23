from fast_depends import inject, Depends

from application.enums import OutputEventType
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
    UnitsSalesFetchInteractor,
)
from logger import create_logger
from time_helpers import Period
from parsers import (
    to_dodo_is_api_account_names,
    merge_account_tokens_and_units,
)
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

    units_sales_fetch_interactor = UnitsSalesFetchInteractor(
        dodo_is_api_connection=dodo_is_api_connection,
        accounts_tokens_and_unit_uuids=accounts_tokens_and_unit_uuids,
        period=Period.today_to_this_time(),
    )

    units_sales_fetch_results_for_today = await units_sales_fetch_interactor.fetch_all()

    logger.info(
        "Fetched units sales for today: %s", units_sales_fetch_results_for_today
    )

    units_sales_fetch_interactor = UnitsSalesFetchInteractor(
        dodo_is_api_connection=dodo_is_api_connection,
        accounts_tokens_and_unit_uuids=accounts_tokens_and_unit_uuids,
        period=Period.week_before_today_to_this_time(),
    )

    units_sales_fetch_results_for_week_before = (
        await units_sales_fetch_interactor.fetch_all()
    )

    logger.info(
        "Fetched units sales for week before: %s",
        units_sales_fetch_results_for_week_before,
    )

    report_generator = SalesStatisticsReportGenerator(
        event=event,
        unit_sales_fetch_results_for_today=units_sales_fetch_results_for_today,
        unit_sales_fetch_results_for_week_before=units_sales_fetch_results_for_week_before,
    )

    sales_statistics = report_generator.get_report()

    logger.info("Sales statistics report: %s", sales_statistics)

    return SpecificChatsEvent[SalesStatistics](
        type=OutputEventType.SALES_STATISTICS,
        chat_ids=event.chat_ids,
        payload=sales_statistics,
    )
