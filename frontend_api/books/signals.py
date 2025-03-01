from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from kafka import KafkaProducer
import json
from .models import Book, User, Borrow

# Initialize Kafka producer once
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

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