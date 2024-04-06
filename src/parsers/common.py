from collections.abc import Iterable
from typing import TypeVar

__all__ = ('flatten',)

T = TypeVar('T')


def flatten(nested_items: Iterable[Iterable[T]]) -> list[T]:
    return [
        item
        for items in nested_items
        for item in items
    ]
