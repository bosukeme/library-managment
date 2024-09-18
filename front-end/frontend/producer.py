import json
import pika
import logging

logger = logging.getLogger('frontend')


def send_message_to_backend(message):
    message_body = json.dumps(message)
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='frontend')

    channel.basic_publish(exchange='',
                          routing_key='frontend',
                          body=message_body)

    logger.info(f"Sent: {message_body}")
    connection.close()
