from enum import StrEnum

__all__ = ('LateDeliveryVoucherIssuer',)


class LateDeliveryVoucherIssuer(StrEnum):
    SYSTEM = 'System'
    CONTACT_CENTER = 'ContactCenter'
