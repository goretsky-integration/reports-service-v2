from collections.abc import Generator
from typing import TypeVar

__all__ = ('batched',)

T = TypeVar('T')


def batched(
        items: list[T],
        *,
        batch_size: int,
) -> Generator[list[T], None, None]:
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]
