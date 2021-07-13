# Asyncromus_data_streaming
This repository gives provides a short implementation for asynchronous producer consumer use case using Kafka Stream for message sending.

## 1. Create docker compose yaml file

```
cd Third_party/kafka-docker/
touch docker-compose-expose.yml
```
Add the following code to the yml file

```yml
version: '2'
services:
  zookeeper:
    image: wurstmeister/zookeeper:3.4.6
    ports:
     - "2181:2181"
  kafka:
    build: .
    ports:
     - "9092:9092"
    expose:
     - "9093"
    environment:
      KAFKA_ADVERTISED_LISTENERS: INSIDE://kafka:9093,OUTSIDE://localhost:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: INSIDE:PLAINTEXT,OUTSIDE:PLAINTEXT
      KAFKA_LISTENERS: INSIDE://0.0.0.0:9093,OUTSIDE://0.0.0.0:9092
      KAFKA_INTER_BROKER_LISTENER_NAME: INSIDE
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_CREATE_TOPICS: "topic_test:1:1"
    volumes:
     - /var/run/docker.sock:/var/run/docker.sock
```

## 2. Install Kafka-Python

```
pip install kafka-python
```

## 3. Run producer.py
This will start the producer which will generate the token which will be added to the 
kafka stream. 

```
python producer.py
```

You can change the producer sleep time as per you need.

```python
for j in range(9999):
        print("Iteration", j)
        data1 = {'counter_1': j}
        producer.send('1_topic_test', value=data1)
        sleep(0.5)
        # sleep(5)
        # sleep(10)
```



## 4. Run Consumer.py
This will start the consumer which will listen to kafka stream for token if no 
token in found it will be in suspended state.

```python
python consumer.py
```

## Run producer and consumer without kafka 
For asyncronus use case without kafka.

RUN
```
python async_prod_con.py
```
##### Producer

```python
async def producer(queue):
    while True:
        # produce a token and send it to a consumer
        token = random.random()
        print(f'produced {token}')
        if token < .05:
            break
        await queue.put(token)
        await rnd_sleep(.1)
```
###### Consumer

```python
async def consumer(queue):
    while True:
        token = await queue.get()
        # process the token received from a producer
        await rnd_sleep(.3)
        queue.task_done()
        print(f'consumed {token}')
```

