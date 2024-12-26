from enum import StrEnum, auto


__all__ = ("QueueName",)


class QueueName(StrEnum):
    SPECIFIC_CHATS_EVENT = "specific-chats-event"
    SALES_STATISTICS = auto()
    STAFF_MEMBERS_BIRTHDAYS = auto()
