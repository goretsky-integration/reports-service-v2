from enum import StrEnum, auto

__all__ = ('ErrorCode',)


class ErrorCode(StrEnum):
    INVALID_AUTH_CREDENTIALS = auto()
    UNEXPECTED_ERROR = auto()
