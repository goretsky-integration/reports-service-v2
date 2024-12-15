from faststream.rabbit import RabbitRouter

from . import late_delivery_vouchers, sales_statistics

__all__ = ('router',)


router = RabbitRouter()
router.include_routers(
    late_delivery_vouchers.router,
    sales_statistics.router,
)
