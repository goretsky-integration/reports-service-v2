import contextlib
from collections.abc import Iterable
from datetime import datetime
from uuid import UUID

import httpx
from pydantic import SecretStr

from enums import CountryCode
from new_types import DodoIsApiConnectionHttpClient

__all__ = (
    'stringify_uuids',
    'closing_dodo_is_api_connection_http_client',
    'DodoIsApiConnection',
    'build_headers',
    'build_request_query_params',
)


def stringify_uuids(uuids: Iterable[UUID]) -> str:
    return ','.join(uuid.hex for uuid in uuids)


def build_request_query_params(
        *,
        from_datetime: datetime,
        to_datetime: datetime,
        unit_uuids: Iterable[UUID],
) -> dict[str, str]:
    return {
        'from': f'{from_datetime:%Y-%m-%dT%H:%M:%S}',
        'to': f'{to_datetime:%Y-%m-%dT%H:%M:%S}',
        'units': stringify_uuids(unit_uuids),
    }


@contextlib.asynccontextmanager
async def closing_dodo_is_api_connection_http_client(
        *,
        country_code: CountryCode,
        timeout: int | float | None,
        user_agent: str | None = None,
) -> DodoIsApiConnectionHttpClient:
    base_url = f'https://api.dodois.io/dodopizza/{country_code}'

    headers = {}
    if user_agent is not None:
        headers['User-Agent'] = user_agent

    async with httpx.AsyncClient(
            base_url=base_url,
            headers=headers,
            timeout=timeout,
    ) as http_client:
        yield http_client


def build_headers(*, access_token: SecretStr) -> dict[str, str]:
    return {
        'Authorization': f'Bearer {access_token.get_secret_value()}',
    }


class DodoIsApiConnection:

    def __init__(self, http_client: DodoIsApiConnectionHttpClient):
        self.__http_client = http_client

    async def get_late_delivery_vouchers(
            self,
            *,
            access_token: SecretStr,
            from_datetime: datetime,
            to_datetime: datetime,
            unit_uuids: Iterable[UUID],
    ) -> httpx.Response:
        request_query_params = build_request_query_params(
            from_datetime=from_datetime,
            to_datetime=to_datetime,
            unit_uuids=unit_uuids,
        )
        url = '/delivery/vouchers'
        headers = build_headers(access_token=access_token)
        return await self.__http_client.get(
            url=url,
            params=request_query_params,
            headers=headers,
        )

    async def get_delivery_statistics(
            self,
            *,
            access_token: SecretStr,
            from_datetime: datetime,
            to_datetime: datetime,
            unit_uuids: Iterable[UUID],
    ) -> httpx.Response:
        request_query_params = build_request_query_params(
            from_datetime=from_datetime,
            to_datetime=to_datetime,
            unit_uuids=unit_uuids,
        )
        url = '/delivery/statistics'
        headers = build_headers(access_token=access_token)
        return await self.__http_client.get(
            url=url,
            params=request_query_params,
            headers=headers,
        )

    async def get_production_productivity(
            self,
            *,
            access_token: SecretStr,
            from_datetime: datetime,
            to_datetime: datetime,
            unit_uuids: Iterable[UUID],
    ) -> httpx.Response:
        """
        Retrieve performance metrics for the selected period
        and specified pizzerias (units).

        Keyword Args:
            unit_uuids: Up to 30 unit UUIDs can be listed in one request.
            from_datetime: The date range start.
            to_datetime: The date range end. It must not exceed 31 days.
            access_token: Access token.

        How the "Speed" Metric is Calculated:

        Speed is the percentage of products prepared faster than
        the established standard time.
        To calculate speed, the number of products prepared on time for a period
        is divided by the total number of products for that period.
        ⚠️ Daily speed is not calculated as the average speed for shifts.

        Shift 1: Prepared 10 products on time out of 100 total.
        Speed for the shift: 10 / 100 = 10%.

        Shift 2: Prepared 50 products on time out of 150 total.
        Speed for the shift: 50 / 150 = 30%.

        The speed metric will be calculated as (10 + 50) / (100 + 150) = 24.
        If you calculate the average per shift,
        the result will be incorrect: (10 + 30) / 2 = 20.

        References:
            Documentation: https://docs.dodois.io/docs/dodo-is/0693bf4a07b8e-proizvodstvo-proizvoditelnost

        Scopes:
            - productionefficiency - production efficiency.

        Returns:
            httpx.Response.
        """
        request_query_params = build_request_query_params(
            from_datetime=from_datetime,
            to_datetime=to_datetime,
            unit_uuids=unit_uuids,
        )
        url = '/production/productivity'
        headers = build_headers(access_token=access_token)
        return await self.__http_client.get(
            url=url,
            params=request_query_params,
            headers=headers,
        )
