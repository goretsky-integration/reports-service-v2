import asyncio

from faststream import FastStream
from faststream.rabbit import RabbitBroker
from pydantic import BaseModel

broker = RabbitBroker('amqp://localhost:5672')
app = FastStream(broker)


class Message(BaseModel):
    unit_id: int


class User(BaseModel):
    name: str


async def main():
    async with broker:
        await broker.publish(
            {
                'chat_ids': [896678539,],
                'unit_uuids': ['000d3a26-b5b0-80f1-11e7-c46eaf0afc18',
                               '000d3a24-0c71-9a87-11e6-8aba13f80da9',
                               '000d3a24-0c71-9a87-11e6-8aba13f82835',
                               '000d3a24-0c71-9a87-11e6-8aba13f88754',
                               'b2026196-fb78-8c1e-11ed-3e2ed037e3e9',
                               '000d3a24-0c71-9a87-11e6-8aba13f8efdf',
                               '000d3a29-ff6b-a943-11e8-7394a1606436',
                               'ee040d87-ae79-9eb6-11ed-22dc5416fd02',
                               '000d3a24-0c71-9a87-11e6-8aba13f9d0ee',
                               '2efce17d-4769-9cfb-11ec-f0679180d18b',
                               '000d3aac-977b-bb2d-11ec-82bbeeb26721',
                               '000d3a39-d824-a82e-11e9-fc73824dc8fd',
                               '000d3a39-d824-a82e-11e9-d84f7dc01968',
                               '000d3a21-da51-a812-11e9-4006b9ffe7fd',
                               '000d3a39-d824-a816-11e9-4006175e1abe',
                               '000d3a29-ff6b-a94b-11e8-f8724c1192bb',
                               '000d3a28-4715-a958-11e8-333d3ee202d9',
                               '000d3a22-31e0-a952-11e8-333d2d4504dd',
                               '000d3a25-8645-a954-11e8-333d19605def',
                               '000d3a22-31e0-a952-11e8-333cdd920305',
                               '000d3a28-4715-a958-11e8-333ccf6cf1a0',
                               '000d3a25-8645-a954-11e8-333ca08c625f',
                               '000d3a28-4715-a956-11e8-2dcf25c462c3',
                               '000d3a25-8645-a94d-11e8-006460706ab4',
                               '000d3a21-55a1-80e4-11e7-9a1a1e9c37ac',
                               '000d3a26-b5b0-80de-11e7-02b7926eda73',
                               '000d3a23-b0dc-80d9-11e6-b24f4a188a9f',
                               '220ece1a-f30a-9f46-11ed-4958027557a6',
                               '000d3a39-d824-a82e-11e9-dacc71d4cdf1',
                               '000d3a24-80c3-810e-11e7-bd751c665f09']
            },
            'late-delivery-vouchers',
        )


if __name__ == '__main__':
    asyncio.run(main())
