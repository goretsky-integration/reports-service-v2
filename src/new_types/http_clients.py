from typing import NewType

import httpx

__all__ = (
    'AuthCredentialsStorageConnectionHttpClient',
    'UnitsStorageConnectionHttpClient',
    'DodoIsApiConnectionHttpClient',
)

AuthCredentialsStorageConnectionHttpClient = NewType(
    'AuthCredentialsStorageConnectionHttpClient',
    httpx.AsyncClient,
)
UnitsStorageConnectionHttpClient = NewType(
    'UnitsStorageConnectionHttpClient',
    httpx.AsyncClient,
)
DodoIsApiConnectionHttpClient = NewType(
    'DodoIsApiConnectionHttpClient',
    httpx.AsyncClient,
)
