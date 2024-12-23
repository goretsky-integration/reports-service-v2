from uuid import UUID
from pydantic import BaseModel, SecretStr

__all__ = ("AccountTokens", "AccountTokensAndUnitUUIDs")


class AccountTokens(BaseModel):
    account_name: str
    access_token: SecretStr
    refresh_token: SecretStr


class AccountTokensAndUnitUUIDs(BaseModel):
    access_token: SecretStr
    unit_uuids: list[UUID]
