from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from kafka import KafkaProducer
import json
from .models import Book

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

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