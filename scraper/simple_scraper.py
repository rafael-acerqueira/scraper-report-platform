import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import os
import json
import csv
import re
from datetime import datetime


def clean_price(price_str):
    """Remove moneatry sign and return a float value"""
    cleaned = re.sub(r'[^\d,\.]', '', price_str)
    cleaned = cleaned.replace(',', '.')
    try:
        return float(cleaned)
    except ValueError:
        return None

def fetch_page(url: str, timeout: int = 10) -> Optional[BeautifulSoup]:
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def scrape_books_from_soup(soup: BeautifulSoup) -> List[Dict]:
    books = []
    for book in soup.select('article.product_pod'):
        title = book.h3.a['title']
        price_text = book.select_one('.price_color').text
        price = clean_price(price_text)
        books.append({'title': title, 'price': price})
    return books

def scrape_books(urls: List[str]) -> List[Dict]:
    """Scrapes multiple URLs and returns a list of all books found."""
    all_books = []
    for url in urls:
        soup = fetch_page(url)
        if soup:
            books = scrape_books_from_soup(soup)
            all_books.extend(books)
    return all_books

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
    books = scrape_books(urls)
    for book in books:
        print(book)
    export_to_json(books)
    export_to_csv(books)
