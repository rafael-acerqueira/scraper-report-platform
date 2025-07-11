from decimal import Decimal

from django.core.management import CommandError
from django.core.management.base import BaseCommand

from scraper import book_scraper

from scraper.registry import get_scraper
from scraper_platform.products.models import Product, ScraperLog
from scraper.utils.export import export_to_json, export_to_csv

URLS = [
    'https://books.toscrape.com/catalogue/page-1.html',
    'https://books.toscrape.com/catalogue/page-2.html',
    'https://books.toscrape.com/catalogue/page-3.html'
]
class Command(BaseCommand):
    help = 'Collects books from the target website and saves to the database'

    def add_arguments(self, parser):
        parser.add_argument('--scraper', required=True, help="Registered scraper name (example: books)")

    def handle(self, *args, **options):
        scraper_name = options['scraper']
        created_count = 0
        status = "success"
        message = ""
        try:
            scraper_cls = get_scraper(scraper_name)
        except ValueError as e:
            status = "error"
            message = str(e)
            ScraperLog.objects.create(
                scraper_name=scraper_name,
                status=status,
                records=created_count,
                message=message,
            )
            raise CommandError(message)

        urls = URLS
        try:
            scraper = scraper_cls(urls)
            items = scraper.scrape()
            for item in items:
                price = Decimal(str(item['price'])) if item.get('price') is not None else Decimal("0.00")
                obj, created = Product.objects.update_or_create(
                    title=item['title'],
                    defaults={'price': price}
                )
                if created:
                    created_count += 1
            export_to_json(items, prefix=scraper_name)
            export_to_csv(items, prefix=scraper_name)
            message = f'Collected and saved {created_count} new products.'
            self.stdout.write(self.style.SUCCESS(message))
            self.stdout.write(self.style.SUCCESS(f'Exported {scraper_name} as JSON and CSV.'))
        except Exception as e:
            status = "error"
            message = str(e)
            self.stdout.write(self.style.ERROR(f"Error during scraping: {message}"))
        finally:

            ScraperLog.objects.create(
                scraper_name=scraper_name,
                status=status,
                records=created_count,
                message=message,
            )