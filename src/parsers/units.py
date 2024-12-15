from collections import defaultdict
from collections.abc import Iterable
from typing import TypeVar
from uuid import UUID

import httpx
from pydantic import TypeAdapter

from models import Unit

__all__ = (
    "parse_units_response",
    "filter_units",
    "group_by_dodo_is_api_account_name",
    "group_by_unit_uuid",
    "to_uuids",
)

T = TypeVar("T", bound=Unit)


def parse_units_response(response: httpx.Response) -> list[Unit]:
    type_adapter = TypeAdapter(list[Unit])
    response_data = response.json()
    return type_adapter.validate_python(response_data["units"])


def filter_units(
    *,
    units: Iterable[Unit],
    allowed_unit_uuids: Iterable[UUID],
) -> list[Unit]:
    allowed_unit_uuids = set(allowed_unit_uuids)
    return [unit for unit in units if unit.uuid in allowed_unit_uuids]


def group_by_dodo_is_api_account_name(
    items: Iterable[T],
) -> dict[str, list[T]]:
    account_name_to_items: defaultdict[str, list[T]] = defaultdict(list)
    for item in items:
        account_name_to_items[item.dodo_is_api_account_name].append(item)
    return dict(account_name_to_items)


def group_by_unit_uuid(items: Iterable[T]) -> dict[UUID, list[T]]:
    unit_uuid_to_items: defaultdict[UUID, list[T]] = defaultdict(list)
    for item in items:
        unit_uuid_to_items[item.uuid].append(item)
    return dict(unit_uuid_to_items)


def to_uuids(items: Iterable[T]) -> list[UUID]:
    return [item.uuid for item in items]
