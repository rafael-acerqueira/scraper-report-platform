from decimal import Decimal

from django.core.management import CommandError
from django.core.management.base import BaseCommand
from scraper import book_scraper

from scraper.registry import get_scraper
from scraper_platform.products.models import Product
from scraper.utils.export import export_to_json, export_to_csv

URLS = [
    'https://books.toscrape.com/catalogue/page-1.html',
    'https://books.toscrape.com/catalogue/page-2.html',
    'https://books.toscrape.com/catalogue/page-3.html'
]

class Command(BaseCommand):
    help = 'Collects books from the target website and saves to the database'

    def add_arguments(self, parser):
        parser.add_argument('--scraper', required=True, help="Registered scrap name (example: books)")

    def handle(self, *args, **options):
        scraper_name = options['scraper']
        try:
            scraper_cls = get_scraper(scraper_name)
        except ValueError as e:
            raise CommandError(str(e))

        urls = [
            'https://books.toscrape.com/catalogue/page-1.html',
            'https://books.toscrape.com/catalogue/page-2.html',
            'https://books.toscrape.com/catalogue/page-3.html'
        ]
        scraper = scraper_cls(urls)
        items = scraper.scrape()
        created_count = 0
        for item in items:
            price = Decimal(str(item['price'])) if item['price'] is not None else Decimal("0.00")
            obj, created = Product.objects.update_or_create(
                title=item['title'],
                defaults={'price': price}
            )
            if created:
                created_count += 1
        self.stdout.write(self.style.SUCCESS(f'Collected and saved {created_count} new products.'))

        export_to_json(items, prefix=scraper_name)
        export_to_csv(items, prefix=scraper_name)
        self.stdout.write(self.style.SUCCESS(f'Exported {scraper_name} to s3_bucket as JSON and CSV.'))