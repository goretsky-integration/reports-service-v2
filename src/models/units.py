from uuid import UUID

from pydantic import BaseModel

__all__ = ('Unit',)


class Unit(BaseModel):
    id: int
    name: str
    uuid: UUID
    office_manager_account_name: str
    dodo_is_api_account_name: str
