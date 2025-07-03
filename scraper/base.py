from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import os
import json
import csv
import re
from datetime import datetime

class BaseScraper(ABC):
    def __init__(self, urls):
        self.urls = urls

    def fetch_page(self, url: str, timeout: int = 10) -> Optional[BeautifulSoup]:
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    @abstractmethod
    def parse(self, soup: BeautifulSoup) -> List[Dict]:
        pass

    def scrape(self) -> List[Dict]:
        all_books = []
        for url in self.urls:
            soup = self.fetch_page(url)
            if soup:
                books = self.parse(soup)
                all_books.extend(books)
        return all_books

    def clean_price(self, price_str):
        cleaned = re.sub(r'[^\d,\.]', '', price_str)
        cleaned = cleaned.replace(',', '.')
        try:
            return float(cleaned)
        except ValueError:
            return None