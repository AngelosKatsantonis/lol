from django.core.management.base import BaseCommand

from sync.client import sync_data_dragon


class Command(BaseCommand):
    def handle(self, *args, **options):
        sync_data_dragon()
