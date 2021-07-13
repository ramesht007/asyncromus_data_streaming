from kafka import KafkaConsumer
from json import loads
from time import sleep
import asyncio

async def rnd_sleep(t):
    # sleep for T seconds on average
    await asyncio.sleep(t * random.random() * 2)

async def consumer():
    queue = asyncio.Queue()

    consumer = KafkaConsumer(
        '1_topic_test',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group-id',
        value_deserializer=lambda x: loads(x.decode('utf-8')))

    for event in consumer:
        event_data = event.value
        print(event_data)
        await queue.put(event_data)

    return queue   


async def receive(queue):
    while True:
        token = await queue.get()
        # process the token received from a producer
        await rnd_sleep(.3)
        queue.task_done()
        print(f'consumed {token}')

asyncio.run(consumer())
asyncio.run(receive(queue))


