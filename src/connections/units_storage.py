from collections.abc import AsyncGenerator
import contextlib

import httpx

from new_types import UnitsStorageConnectionHttpClient

__all__ = (
    "UnitsStorageConnection",
    "closing_units_storage_connection_http_client",
)


@contextlib.asynccontextmanager
async def closing_units_storage_connection_http_client(
    base_url: str,
) -> AsyncGenerator[UnitsStorageConnectionHttpClient, None]:
    async with httpx.AsyncClient(base_url=base_url) as http_client:
        yield UnitsStorageConnectionHttpClient(http_client)


class UnitsStorageConnection:
    def __init__(self, http_client: UnitsStorageConnectionHttpClient):
        self.__http_client = http_client

    async def get_units(self) -> httpx.Response:
        url = "/units/"
        return await self.__http_client.get(url)
