from decimal import Decimal

from django.core.management.base import BaseCommand
from scraper.simple_scraper import BookScraper
from scraper_platform.products.models import Product
from scraper.utils.export import export_to_json, export_to_csv

URLS = [
    'https://books.toscrape.com/catalogue/page-1.html',
    'https://books.toscrape.com/catalogue/page-2.html',
    'https://books.toscrape.com/catalogue/page-3.html'
]

class Command(BaseCommand):
    help = 'Collects books from the target website and saves to the database'

    def handle(self, *args, **kwargs):
        scrape_books = BookScraper(URLS)
        books = scrape_books.scrape()
        created_count = 0
        for book in books:
            price = Decimal(str(book['price'])) if book['price'] is not None else Decimal("0.00")
            obj, created = Product.objects.update_or_create(
                title=book['title'],
                defaults={'price': price}
            )
            if created:
                created_count += 1
        self.stdout.write(self.style.SUCCESS(f'Collected and saved {created_count} new products.'))

        export_to_json(books, output_dir='s3_bucket', prefix='books')
        export_to_csv(books, output_dir='s3_bucket', prefix='books')
        self.stdout.write(self.style.SUCCESS('Exported books to s3_bucket as JSON and CSV.'))