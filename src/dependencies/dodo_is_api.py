from fast_depends import Depends

from config import Config, get_config
from connections import (
    DodoIsApiConnection,
    closing_dodo_is_api_connection_http_client,
)
from new_types import DodoIsApiConnectionHttpClient

__all__ = (
    "get_dodo_is_api_connection_http_client",
    "get_dodo_is_api_connection",
)


async def get_dodo_is_api_connection_http_client(
    config: Config = Depends(get_config, use_cache=True),
) -> DodoIsApiConnectionHttpClient:
    async with closing_dodo_is_api_connection_http_client(
        country_code=config.country_code,
        user_agent="Goretsky-Band",
        timeout=30,
    ) as http_client:
        yield http_client


async def get_dodo_is_api_connection(
    http_client: DodoIsApiConnectionHttpClient = Depends(
        get_dodo_is_api_connection_http_client,
        use_cache=False,
    ),
) -> DodoIsApiConnection:
    return DodoIsApiConnection(http_client)
