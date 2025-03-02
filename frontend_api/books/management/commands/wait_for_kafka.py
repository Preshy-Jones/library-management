from django.core.management.base import BaseCommand
from kafka import KafkaAdminClient
from kafka.errors import NoBrokersAvailable
import time

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Waiting for Kafka...')
        max_retries = 20
        
        for i in range(max_retries):
            try:
                admin = KafkaAdminClient(
                    bootstrap_servers='kafka:9092',
                    api_version=(2, 8, 1))
                admin.list_topics()
                self.stdout.write(self.style.SUCCESS('Kafka is ready!'))
                return
            except NoBrokersAvailable as e:  # Added proper except clause
                self.stdout.write(f'Attempt {i+1}/{max_retries}: Kafka not ready yet...')
                time.sleep(10)
            except Exception as e:  # Catch-all for other errors
                self.stdout.write(f'Unexpected error: {str(e)}')
                time.sleep(10)
        
        self.stdout.write(self.style.ERROR('Failed to connect to Kafka after retries'))
        exit(1)