from dataclasses import dataclass
from typing import TypeVar, Generic
from uuid import UUID


__all__ = ("FetchResult",)


T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class FetchResult(Generic[T]):
    unit_uuids: tuple[UUID, ...]
    data: T | None = None
    exception: Exception | None = None
    error_code: str | None = None
