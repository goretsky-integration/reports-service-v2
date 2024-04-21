import sentry_sdk
from fast_depends import Depends
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from config import Config, get_config
import handlers
from logger import init_logging


def on_startup(
        config: Config = Depends(get_config),
) -> None:
    if config.sentry.is_enabled:
        sentry_sdk.init(
            dsn=config.sentry.dsn.get_secret_value(),
            traces_sample_rate=config.sentry.traces_sample_rate,
            profiles_sample_rate=config.sentry.profiles_sample_rate,
        )
    init_logging()


broker = RabbitBroker('amqp://localhost:5672')
app = FastStream(broker)

broker.include_routers(
    handlers.late_delivery_vouchers.router,
    handlers.delivery_speed.router,
)
app.on_startup(on_startup)
