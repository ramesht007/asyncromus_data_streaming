from time import sleep
from json import dumps
from kafka import KafkaProducer
import asyncio, random


def producer():

    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda x: dumps(x).encode('utf-8'))


    for j in range(9999):
        print("Iteration", j)
        data1 = {'counter_1': j}
        producer.send('1_topic_test', value=data1)
        sleep(0.5)


producer()