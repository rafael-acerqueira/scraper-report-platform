from django.core.management.base import BaseCommand
from scraper.registry import _SCRAPER_REGISTRY

class Command(BaseCommand):
    help = "List all scrapers registered"

    def handle(self, *args, **kwargs):
        if not _SCRAPER_REGISTRY:
            self.stdout.write("No registered scrapers.")
        else:
            self.stdout.write("Scrapers available:")
            for name in _SCRAPER_REGISTRY:
                self.stdout.write(f" - {name}")