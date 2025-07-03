from scraper import book_scraper
from scraper.registry import get_scraper



def run_all_scrapers():
    all_items = []
    for scraper_name in ['books']:
        scraper_cls = get_scraper(scraper_name)
        urls= [
            'https://books.toscrape.com/catalogue/page-1.html',
            'https://books.toscrape.com/catalogue/page-2.html',
            'https://books.toscrape.com/catalogue/page-3.html'
        ]
        scraper = scraper_cls(urls)
        all_items.extend(scraper.scrape())
    return all_items

if __name__ == '__main__':
    items = run_all_scrapers()
    print(items)