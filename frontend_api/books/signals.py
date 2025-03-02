from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import json
from .models import Book, User, Borrow
import logging
import time

from .models import Book  # Change to your admin models

logger = logging.getLogger(__name__)

def get_kafka_producer():
    max_retries = 5
    for _ in range(max_retries):
        try:
            return KafkaProducer(
                bootstrap_servers='kafka:9092',
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                api_version=(2, 8, 1)
            )
        except NoBrokersAvailable:
            logger.warning("Kafka broker not available, retrying...")
            time.sleep(5)
    logger.error("Failed to connect to Kafka after multiple retries")
    return None

producer = get_kafka_producer()
@receiver(post_save, sender=User)
def user_created_handler(sender, instance, created, **kwargs):
    """Send user data to admin service when new user enrolls"""
    if created:
        producer.send('users_topic', {
            'action': 'create',
            'user_id': instance.id,
            'email': instance.email,
            'firstname': instance.firstname,
            'lastname': instance.lastname
        })

@receiver(post_save, sender=Borrow)
def borrow_created_handler(sender, instance, created, **kwargs):
    """Notify admin service about book borrows"""
    if created:
        producer.send('borrows_topic', {
            'action': 'create',
            'user_id': instance.user.id,
            'book_id': instance.book.id,
            'due_date': instance.due_date.isoformat()
        })