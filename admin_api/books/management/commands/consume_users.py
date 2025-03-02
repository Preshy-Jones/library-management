from django.core.management.base import BaseCommand
from kafka import KafkaConsumer
import json
from admin.models import User

class Command(BaseCommand):
    help = 'Consumes user events from Kafka'

    def handle(self, *args, **options):
        consumer = KafkaConsumer(
            'users_topic',
            bootstrap_servers='kafka:9092',
            auto_offset_reset='earliest',
            group_id='admin-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

        for message in consumer:
            data = message.value
            User.objects.create(
                id=data['user_id'],
                email=data['email'],
                firstname=data['firstname'],
                lastname=data['lastname']
            )