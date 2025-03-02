from django.core.management.base import BaseCommand
from kafka import KafkaConsumer
import json
from admin.models import Borrow, User, Book
from django.utils.dateparse import parse_date

class Command(BaseCommand):
    help = 'Consumes borrow events from Kafka'

    def handle(self, *args, **options):
        consumer = KafkaConsumer(
            'borrows_topic',
            bootstrap_servers='kafka:9092',
            auto_offset_reset='earliest',
            group_id='admin-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

        for message in consumer:
            data = message.value
            user = User.objects.get(id=data['user_id'])
            book = Book.objects.get(id=data['book_id'])
            due_date = parse_date(data['due_date'])
            Borrow.objects.create(
                user=user,
                book=book,
                due_date=due_date
            )