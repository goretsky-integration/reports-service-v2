from typing import Annotated, TypeVar, Generic
from pydantic import BaseModel, Field

from models.units import Unit

__all__ = ("Event", "SpecificChatsEvent")


T = TypeVar("T")


class Event(BaseModel):
    units: Annotated[list[Unit], Field(min_length=1)]
    chat_ids: set[int]


class SpecificChatsEvent(BaseModel, Generic[T]):
    """Output from handlers event."""

    type: str
    payload: T
    chat_ids: set[int]
