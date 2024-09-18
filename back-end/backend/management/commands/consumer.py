import json
import pika
import logging

from django.core.management.base import BaseCommand
from backend.service import sort_receive_message

logger = logging.getLogger('backend')


class Command(BaseCommand):
    help = 'Consumes messages from RabbitMQ queue'

    def handle(self, *args, **options):
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()

        # Declare the queue
        channel.queue_declare(queue='frontend')

        # Define the callback function
        def callback(ch, method, properties, body):
            try:
                message = json.loads(body)
                logger.info(f"Received: {body}")
                sort_receive_message(message)

            except json.JSONDecodeError as e:
                logger.error(f"Error decoding JSON: {e}")

        channel.basic_consume(queue='frontend', on_message_callback=callback, auto_ack=True)

        logger.info("[*] Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()
