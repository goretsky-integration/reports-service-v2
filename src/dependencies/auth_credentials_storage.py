from collections.abc import AsyncGenerator
from fast_depends import Depends

from config import Config, get_config
from connections import (
    AuthCredentialsStorageConnection,
    closing_auth_credentials_storage_connection_http_client,
)
from new_types import AuthCredentialsStorageConnectionHttpClient

__all__ = (
    "get_auth_credentials_storage_connection_http_client",
    "get_auth_credentials_storage_connection",
)


async def get_auth_credentials_storage_connection_http_client(
    config: Config = Depends(get_config, use_cache=True),
) -> AsyncGenerator[AuthCredentialsStorageConnectionHttpClient]:
    async with closing_auth_credentials_storage_connection_http_client(
        base_url=str(config.auth_credentials_storage_base_url),
    ) as http_client:
        yield AuthCredentialsStorageConnectionHttpClient(http_client)


async def get_auth_credentials_storage_connection(
    http_client: AuthCredentialsStorageConnectionHttpClient = Depends(
        get_auth_credentials_storage_connection_http_client,
        use_cache=False,
    ),
) -> AuthCredentialsStorageConnection:
    return AuthCredentialsStorageConnection(http_client)
