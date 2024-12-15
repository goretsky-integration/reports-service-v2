from collections.abc import Generator, Iterable
from typing import TypeVar

__all__ = ("batched",)

T = TypeVar("T")


def batched(
    items: Iterable[T],
    *,
    batch_size: int,
) -> Generator[tuple[T, ...], None, None]:
    items = tuple(items)
    for i in range(0, len(items), batch_size):
        yield items[i : i + batch_size]
