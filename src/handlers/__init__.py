from faststream.rabbit import RabbitRouter

from . import late_delivery_vouchers, revenue

__all__ = ('router',)


router = RabbitRouter()
router.include_routers(
    late_delivery_vouchers.router,
    revenue.router,
)
