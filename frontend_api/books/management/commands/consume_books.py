from django.core.management.base import BaseCommand
from kafka import KafkaConsumer
import json
from books.models import Book

class Command(BaseCommand):
    help = 'Consumes book events from Kafka'

    def handle(self, *args, **options):
        consumer = KafkaConsumer(
            'books_topic',
            bootstrap_servers='kafka:9092',
            auto_offset_reset='earliest',
            group_id='frontend-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

        for message in consumer:
            data = message.value
            action = data.get('action')
            if action == 'create':
                Book.objects.create(
                    id=data['book_id'],
                    title=data['title'],
                    publisher=data['publisher'],
                    category=data['category'],
                    available=True
                )
            elif action == 'delete':
                Book.objects.filter(id=data['book_id']).delete()