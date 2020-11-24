from django.core.management.base import BaseCommand

from sync.game_assets_client import sync_game_assets


class Command(BaseCommand):
    def handle(self, *args, **options):
        sync_game_assets()
