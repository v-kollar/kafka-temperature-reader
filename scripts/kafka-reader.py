import os
import uuid
import json
from kafka import KafkaConsumer

MIN_TEMPERATURE = -10
MAX_TEMPERATURE = 30

KAFKA_BROKERS = os.getenv('KAFKA_BROKERS', 'localhost:9092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'temperature')
CONSUMER_GROUP = os.getenv('CONSUMER_GROUP', 'temperature_reader')
INSTANCE_ID = uuid.uuid4()

def init_consumer(topic, brokers, group):
    return KafkaConsumer(
        topic,
        bootstrap_servers=brokers,
        auto_offset_reset='latest',
        group_id=group
       )


def is_required_temperature(value):
    return 'sensor_id' in value and 'temperature' in value \
           and MIN_TEMPERATURE <= value['temperature'] <= MAX_TEMPERATURE


def process_messages(consumer):
    for message in consumer:
        if message.value is not None:
            parsed_value = None
            try:
                parsed_value = json.loads(message.value)
            except json.JSONDecodeError:
                continue

            if is_required_temperature(parsed_value):
                print(f'{INSTANCE_ID} {parsed_value}', flush=True)



if __name__ == '__main__':
    consumer = init_consumer(KAFKA_TOPIC, KAFKA_BROKERS, CONSUMER_GROUP)
    process_messages(consumer)

