from faststream import FastStream

from logger import setup_logging
from faststream.rabbit import RabbitBroker
from handlers.router import router


broker = RabbitBroker("amqp://localhost:5672")
app = FastStream(broker)


@app.on_startup
async def on_startup() -> None:
    broker.include_router(router)
    setup_logging()
