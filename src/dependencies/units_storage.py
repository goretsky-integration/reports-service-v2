from fast_depends import Depends

from config import Config, get_config
from connections import (
    UnitsStorageConnection,
    closing_units_storage_connection_http_client,
)
from new_types import UnitsStorageConnectionHttpClient

__all__ = (
    'get_units_storage_connection_http_client',
    'get_units_storage_connection',
)


async def get_units_storage_connection_http_client(
        config: Config = Depends(get_config, use_cache=True)
) -> UnitsStorageConnectionHttpClient:
    async with closing_units_storage_connection_http_client(
            base_url=str(config.units_storage_base_url),
    ) as http_client:
        yield http_client


async def get_units_storage_connection(
        http_client: UnitsStorageConnectionHttpClient = Depends(
            get_units_storage_connection_http_client,
            use_cache=False,
        )
) -> UnitsStorageConnection:
    return UnitsStorageConnection(http_client)
