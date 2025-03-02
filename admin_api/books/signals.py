from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import json
from .models import Book
import logging
import time
import json
from kafka.errors import NoBrokersAvailable
from kafka import KafkaProducer
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

@receiver(post_save, sender=Book)
def book_created_handler(sender, instance, created, **kwargs):
    """Sync new books to frontend service"""
    if created:
        producer.send('books_topic', {
            'action': 'create',
            'book_id': instance.id,
            'title': instance.title,
            'publisher': instance.publisher,
            'category': instance.category
        })

@receiver(post_delete, sender=Book)
def book_deleted_handler(sender, instance, **kwargs):
    """Notify frontend about book deletions"""
    producer.send('books_topic', {
        'action': 'delete',
        'book_id': instance.id
    })