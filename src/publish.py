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
                'chat_ids': [896678539, ],
                'units': [
                    {
                        "id": 1398,
                        "name": "Подольск-3",
                        "uuid": "220ece1a-f30a-9f46-11ed-4958027557a6",
                        "office_manager_account_name": "office_manager_podolsk",
                        "dodo_is_api_account_name": "api_msk_4_and_podolsk",
                        "region": "Москва 4"
                    },
                    {
                        "id": 1047,
                        "name": "Подольск-2",
                        "uuid": "000d3a39-d824-a82e-11e9-dacc71d4cdf1",
                        "office_manager_account_name": "office_manager_podolsk",
                        "dodo_is_api_account_name": "api_msk_4_and_podolsk",
                        "region": "Москва 4"
                    },
                    {
                        "id": 605,
                        "name": "Подольск-1",
                        "uuid": "000d3a24-80c3-810e-11e7-bd751c665f09",
                        "office_manager_account_name": "office_manager_podolsk",
                        "dodo_is_api_account_name": "api_msk_4_and_podolsk",
                        "region": "Москва 4"
                    },
                    {
                        "id": 969,
                        "name": "Москва 4-16",
                        "uuid": "000d3a21-da51-a812-11e9-40067acb1091",
                        "office_manager_account_name": "office_manager_msk_4",
                        "dodo_is_api_account_name": "api_msk_4_and_podolsk",
                        "region": "Москва 4"
                    },
                    {
                        "id": 1374,
                        "name": "Москва 4-9",
                        "uuid": "2efce17d-4769-9cfb-11ec-f0679180d18b",
                        "office_manager_account_name": "office_manager_msk_4",
                        "dodo_is_api_account_name": "api_msk_4_and_podolsk",
                        "region": "Москва 4"
                    },
                    {
                        "id": 1341,
                        "name": "Москва 4-8",
                        "uuid": "000d3aac-977b-bb2d-11ec-82bbeeb26721",
                        "office_manager_account_name": "office_manager_msk_4",
                        "dodo_is_api_account_name": "api_msk_4_and_podolsk",
                        "region": "Москва 4"
                    },
                    {
                        "id": 1066,
                        "name": "Москва 4-19",
                        "uuid": "000d3a39-d824-a82e-11e9-fc73824dc8fd",
                        "office_manager_account_name": "office_manager_msk_4",
                        "dodo_is_api_account_name": "api_msk_4_and_podolsk",
                        "region": "Москва 4"
                    },
                    {
                        "id": 1046,
                        "name": "Москва 4-18",
                        "uuid": "000d3a39-d824-a82e-11e9-d84f7dc01968",
                        "office_manager_account_name": "office_manager_msk_4",
                        "dodo_is_api_account_name": "api_msk_4_and_podolsk",
                        "region": "Москва 4"
                    },
                    {
                        "id": 970,
                        "name": "Москва 4-17",
                        "uuid": "000d3a21-da51-a812-11e9-4006b9ffe7fd",
                        "office_manager_account_name": "office_manager_msk_4",
                        "dodo_is_api_account_name": "api_msk_4_and_podolsk",
                        "region": "Москва 4"
                    },
                    {
                        "id": 968,
                        "name": "Москва 4-15",
                        "uuid": "000d3a39-d824-a816-11e9-4006175e1abe",
                        "office_manager_account_name": "office_manager_msk_4",
                        "dodo_is_api_account_name": "api_msk_4_and_podolsk",
                        "region": "Москва 4"
                    },
                    {
                        "id": 919,
                        "name": "Москва 4-14",
                        "uuid": "000d3a29-ff6b-a94b-11e8-f8724c1192bb",
                        "office_manager_account_name": "office_manager_msk_4",
                        "dodo_is_api_account_name": "api_msk_4_and_podolsk",
                        "region": "Москва 4"
                    },
                    {
                        "id": 719,
                        "name": "Москва 4-13",
                        "uuid": "000d3a28-4715-a958-11e8-333d3ee202d9",
                        "office_manager_account_name": "office_manager_msk_4",
                        "dodo_is_api_account_name": "api_msk_4_and_podolsk",
                        "region": "Москва 4"
                    },
                    {
                        "id": 718,
                        "name": "Москва 4-12",
                        "uuid": "000d3a22-31e0-a952-11e8-333d2d4504dd",
                        "office_manager_account_name": "office_manager_msk_4",
                        "dodo_is_api_account_name": "api_msk_4_and_podolsk",
                        "region": "Москва 4"
                    },
                    {
                        "id": 717,
                        "name": "Москва 4-11",
                        "uuid": "000d3a25-8645-a954-11e8-333d19605def",
                        "office_manager_account_name": "office_manager_msk_4",
                        "dodo_is_api_account_name": "api_msk_4_and_podolsk",
                        "region": "Москва 4"
                    },
                    {
                        "id": 714,
                        "name": "Москва 4-7",
                        "uuid": "000d3a22-31e0-a952-11e8-333cdd920305",
                        "office_manager_account_name": "office_manager_msk_4",
                        "dodo_is_api_account_name": "api_msk_4_and_podolsk",
                        "region": "Москва 4"
                    },
                    {
                        "id": 713,
                        "name": "Москва 4-6",
                        "uuid": "000d3a28-4715-a958-11e8-333ccf6cf1a0",
                        "office_manager_account_name": "office_manager_msk_4",
                        "dodo_is_api_account_name": "api_msk_4_and_podolsk",
                        "region": "Москва 4"
                    },
                    {
                        "id": 712,
                        "name": "Москва 4-5",
                        "uuid": "000d3a25-8645-a954-11e8-333ca08c625f",
                        "office_manager_account_name": "office_manager_msk_4",
                        "dodo_is_api_account_name": "api_msk_4_and_podolsk",
                        "region": "Москва 4"
                    },
                    {
                        "id": 708,
                        "name": "Москва 4-4",
                        "uuid": "000d3a28-4715-a956-11e8-2dcf25c462c3",
                        "office_manager_account_name": "office_manager_msk_4",
                        "dodo_is_api_account_name": "api_msk_4_and_podolsk",
                        "region": "Москва 4"
                    },
                    {
                        "id": 652,
                        "name": "Москва 4-3",
                        "uuid": "000d3a25-8645-a94d-11e8-006460706ab4",
                        "office_manager_account_name": "office_manager_msk_4",
                        "dodo_is_api_account_name": "api_msk_4_and_podolsk",
                        "region": "Москва 4"
                    },
                    {
                        "id": 582,
                        "name": "Москва 4-10",
                        "uuid": "000d3a21-55a1-80e4-11e7-9a1a1e9c37ac",
                        "office_manager_account_name": "office_manager_msk_4",
                        "dodo_is_api_account_name": "api_msk_4_and_podolsk",
                        "region": "Москва 4"
                    },
                    {
                        "id": 436,
                        "name": "Москва 4-2",
                        "uuid": "000d3a26-b5b0-80de-11e7-02b7926eda73",
                        "office_manager_account_name": "office_manager_msk_4",
                        "dodo_is_api_account_name": "api_msk_4_and_podolsk",
                        "region": "Москва 4"
                    },
                    {
                        "id": 389,
                        "name": "Москва 4-1",
                        "uuid": "000d3a23-b0dc-80d9-11e6-b24f4a188a9f",
                        "office_manager_account_name": "office_manager_msk_4",
                        "dodo_is_api_account_name": "api_msk_4_and_podolsk",
                        "region": "Москва 4"
                    },
                    {
                        "id": 152,
                        "name": "Калуга-1",
                        "uuid": "000d3a24-0c71-9a87-11e6-8aba13f8efdf",
                        "office_manager_account_name": "office_manager_kaluga",
                        "dodo_is_api_account_name": "api_smoluga",
                        "region": "Калуга"
                    },
                    {
                        "id": 821,
                        "name": "Калуга-2",
                        "uuid": "000d3a29-ff6b-a943-11e8-7394a1606436",
                        "office_manager_account_name": "office_manager_kaluga",
                        "dodo_is_api_account_name": "api_smoluga",
                        "region": "Калуга"
                    },
                    {
                        "id": 1387,
                        "name": "Калуга-3",
                        "uuid": "ee040d87-ae79-9eb6-11ed-22dc5416fd02",
                        "office_manager_account_name": "office_manager_kaluga",
                        "dodo_is_api_account_name": "api_smoluga",
                        "region": "Калуга"
                    },
                    {
                        "id": 9,
                        "name": "Смоленск-1",
                        "uuid": "000d3a24-0c71-9a87-11e6-8aba13f80da9",
                        "office_manager_account_name": "office_manager_smolensk",
                        "dodo_is_api_account_name": "api_smoluga",
                        "region": "Смоленск"
                    },
                    {
                        "id": 24,
                        "name": "Смоленск-2",
                        "uuid": "000d3a24-0c71-9a87-11e6-8aba13f82835",
                        "office_manager_account_name": "office_manager_smolensk",
                        "dodo_is_api_account_name": "api_smoluga",
                        "region": "Смоленск"
                    },
                    {
                        "id": 83,
                        "name": "Смоленск-3",
                        "uuid": "000d3a24-0c71-9a87-11e6-8aba13f88754",
                        "office_manager_account_name": "office_manager_smolensk",
                        "dodo_is_api_account_name": "api_smoluga",
                        "region": "Смоленск"
                    },
                    {
                        "id": 1395,
                        "name": "Смоленск-4",
                        "uuid": "b2026196-fb78-8c1e-11ed-3e2ed037e3e9",
                        "office_manager_account_name": "office_manager_smolensk",
                        "dodo_is_api_account_name": "api_smoluga",
                        "region": "Смоленск"
                    },
                    {
                        "id": 609,
                        "name": "Вязьма-1",
                        "uuid": "000d3a26-b5b0-80f1-11e7-c46eaf0afc18",
                        "office_manager_account_name": "office_manager_vyazma",
                        "dodo_is_api_account_name": "api_smoluga",
                        "region": "Смоленск"
                    },
                    {
                        "id": 300,
                        "name": "Обнинск-1",
                        "uuid": "000d3a24-0c71-9a87-11e6-8aba13f9d0ee",
                        "office_manager_account_name": "office_manager_obninsk",
                        "dodo_is_api_account_name": "api_smoluga",
                        "region": "Калуга"
                    }
                ]
            },
            'sales-statistics',
        )


if __name__ == '__main__':
    asyncio.run(main())
