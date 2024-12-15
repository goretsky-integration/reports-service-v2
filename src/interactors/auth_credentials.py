import asyncio
from collections.abc import Iterable
from dataclasses import dataclass

from pydantic import ValidationError

from models.auth_credentials import AccountTokens
from enums import ErrorCode
from dependencies.auth_credentials_storage import (
    AuthCredentialsStorageConnection,
)
from parsers.auth_credentials import parse_account_tokens_response
from logger import create_logger


__all__ = (
    "AuthTokensFetchResult",
    "AuthTokensFetchInteractor",
)


logger = create_logger("auth_credentials")


@dataclass(frozen=True, slots=True)
class AuthTokensFetchResult:
    account_name: str
    data: AccountTokens | None = None
    exception: Exception | None = None
    error_code: ErrorCode | None = None


class AuthTokensFetchInteractor:
    def __init__(
        self,
        *,
        auth_credentials_storage_connection: AuthCredentialsStorageConnection,
        account_names: Iterable[str],
    ):
        self.__auth_credentials_storage_connection = auth_credentials_storage_connection
        self.__account_names = tuple(account_names)

    async def fetch_one(self, account_name: str) -> AuthTokensFetchResult:
        response = await self.__auth_credentials_storage_connection.get_tokens(
            account_name=account_name,
        )
        try:
            account_tokens = parse_account_tokens_response(response)
        except ValidationError as error:
            return AuthTokensFetchResult(
                account_name=account_name,
                exception=error,
                error_code=ErrorCode.INVALID_AUTH_CREDENTIALS,
            )
        except Exception as error:
            logger.error(
                "Unexpected error fetching tokens for %s: %s",
                account_name,
                str(error),
            )
            return AuthTokensFetchResult(
                account_name=account_name,
                exception=error,
                error_code=ErrorCode.UNEXPECTED_ERROR,
            )
        return AuthTokensFetchResult(
            account_name=account_name,
            data=account_tokens,
        )

    async def fetch_all(self) -> list[AuthTokensFetchResult]:
        tasks: list[asyncio.Task[AuthTokensFetchResult]] = []

        async with asyncio.TaskGroup() as task_group:
            for account_name in self.__account_names:
                task = task_group.create_task(self.fetch_one(account_name))
                tasks.append(task)

        return [task.result() for task in tasks]
