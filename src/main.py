from faststream import FastStream
from faststream.rabbit import RabbitBroker

from handlers import router
from src.logger import setup_logging


broker = RabbitBroker("amqp://localhost:5672")
app = FastStream(broker)

broker.include_router(router)


@app.on_startup
async def on_startup() -> None:
    setup_logging()
