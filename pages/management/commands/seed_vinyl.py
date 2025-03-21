from django.core.management.base import BaseCommand
from pages.factories import VinylFactory

class Command(BaseCommand):
    help = 'Seed the database with vinyl'

    def handle(self, *args, **kwargs):
        VinylFactory.create_batch(8)
        self.stdout.write(self.style.SUCCESS('Successfully seeded Vinyl'))