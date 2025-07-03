from scraper import book_scraper, quote_scraper
from scraper.registry import get_scraper

SCRAPERS_TO_RUN = {
    'books': [
        'https://books.toscrape.com/catalogue/page-1.html',
        'https://books.toscrape.com/catalogue/page-2.html',
        'https://books.toscrape.com/catalogue/page-3.html',
    ],
    'quotes': [
        'https://quotes.toscrape.com/page/1/',
        'https://quotes.toscrape.com/page/2/',
    ]
}

def run_all_scrapers():
    all_items = []
    for scraper_name, urls in SCRAPERS_TO_RUN.items():
        scraper_cls = get_scraper(scraper_name)
        scraper = scraper_cls(urls)
        scraped = scraper.scrape()

        for item in scraped:
            item['source'] = scraper_name
        all_items.extend(scraped)
    return all_items

if __name__ == '__main__':
    items = run_all_scrapers()
    for item in items:
        print(item)