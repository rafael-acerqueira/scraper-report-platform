from .base import BaseScraper
from bs4 import BeautifulSoup
from typing import List, Dict
import os
import json
import csv
from datetime import datetime

class BookScraper(BaseScraper):
    def parse_books(self, soup: BeautifulSoup) -> List[Dict]:
        books = []
        for book in soup.select('article.product_pod'):
            title = book.h3.a['title']
            price_text = book.select_one('.price_color').text
            price = self.clean_price(price_text)
            books.append({'title': title, 'price': price})
        return books


def export_to_json(data, output_dir='scraper/outputs', prefix='books'):
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    path = os.path.join(output_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Exported {len(data)} records to {path}")

def export_to_csv(data, output_dir='scraper/outputs', prefix='books'):
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    path = os.path.join(output_dir, filename)
    if data:
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        print(f"Exported {len(data)} records to {path}")
    else:
        print("No data to export.")

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
