from django.core.management.base import BaseCommand
from scraper.simple_scraper import scrape_books
from scraper_platform.products.models import Product

URLS = [
    'https://books.toscrape.com/catalogue/page-1.html',
    'https://books.toscrape.com/catalogue/page-2.html',
    'https://books.toscrape.com/catalogue/page-3.html'
]

class Command(BaseCommand):
    help = 'Collects books from the target website and saves to the database'

    def handle(self, *args, **kwargs):
        books = scrape_books(URLS)
        created_count = 0
        for book in books:
            obj, created = Product.objects.get_or_create(
                title=book['title'],
                price=book['price']
            )
            if created:
                created_count += 1
        self.stdout.write(self.style.SUCCESS(f'Collected and saved {created_count} new products.'))