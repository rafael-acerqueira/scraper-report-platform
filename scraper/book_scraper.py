from .base import BaseScraper
from bs4 import BeautifulSoup
from typing import List, Dict
from scraper.utils.export import export_to_json, export_to_csv
from .registry import register_scraper

@register_scraper('books')
class BookScraper(BaseScraper):
    def parse(self, soup: BeautifulSoup) -> List[Dict]:
        books = []
        for book in soup.select('article.product_pod'):
            title = book.h3.a['title']
            price_text = book.select_one('.price_color').text
            price = self.clean_price(price_text)
            books.append({'title': title, 'price': price})
        return books

if __name__ == "__main__":
    urls = [
        'https://books.toscrape.com/catalogue/page-1.html',
        'https://books.toscrape.com/catalogue/page-2.html',
        'https://books.toscrape.com/catalogue/page-3.html'
    ]
    scraper = BookScraper(urls)
    books = scraper.scrape()
    for book in books:
        print(book)
    export_to_json(books)
    export_to_csv(books)
