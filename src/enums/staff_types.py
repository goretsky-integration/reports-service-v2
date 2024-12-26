from enum import StrEnum

__all__ = ("StaffType",)


class StaffType(StrEnum):
    OPERATOR = "Operator"
    KITCHEN_MEMBER = "KitchenMember"
    COURIER = "Courier"
    CASHIER = "Cashier"
    PERSONAL_MANAGER = "PersonalManager"
