from collections.abc import AsyncGenerator
import contextlib

import httpx

from new_types import AuthCredentialsStorageConnectionHttpClient
from logger import create_logger

__all__ = (
    "AuthCredentialsStorageConnection",
    "closing_auth_credentials_storage_connection_http_client",
)

logger = create_logger("connections:auth_credentials")


@contextlib.asynccontextmanager
async def closing_auth_credentials_storage_connection_http_client(
    base_url: str,
) -> AsyncGenerator[AuthCredentialsStorageConnectionHttpClient, None]:
    logger.debug("Creating auth credentials storage connection HTTP client")
    async with httpx.AsyncClient(base_url=base_url) as http_client:
        yield AuthCredentialsStorageConnectionHttpClient(http_client)
    logger.debug("Closing auth credentials storage connection HTTP client")


class AuthCredentialsStorageConnection:
    def __init__(
        self,
        http_client: AuthCredentialsStorageConnectionHttpClient,
    ):
        self.__http_client = http_client

    async def get_accounts(self) -> httpx.Response:
        url = "/accounts/"

        response = await self.__http_client.get(url)

        return response

    async def get_cookies(self, account_name: str) -> httpx.Response:
        url = "/auth/cookies/"
        request_query_params = {"account_name": account_name}

        return await self.__http_client.get(
            url=url,
            params=request_query_params,
        )

    async def get_tokens(self, account_name: str) -> httpx.Response:
        url = "/auth/token/"
        request_query_params = {"account_name": account_name}

        return await self.__http_client.get(
            url=url,
            params=request_query_params,
        )
