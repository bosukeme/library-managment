import json
import pika
import logging

logger = logging.getLogger('backend')


def send_message_to_frontend(message):
    message_body = json.dumps(message)
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue='backend')
        channel.basic_publish(exchange='',
                              routing_key='backend',
                              body=message_body)

        logger.info(f"Sent: {message_body}")
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        connection.close()
