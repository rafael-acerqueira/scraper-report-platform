from .base import BaseScraper
from bs4 import BeautifulSoup
from typing import List, Dict
from .registry import register_scraper

@register_scraper('quotes')
class QuoteScraper(BaseScraper):
    def parse(self, soup: BeautifulSoup) -> List[Dict]:
        quotes = []
        for quote in soup.select('div.quote'):
            text = quote.select_one('span.text').text
            author = quote.select_one('small.author').text
            quotes.append({'text': text, 'author': author})
        return quotes

