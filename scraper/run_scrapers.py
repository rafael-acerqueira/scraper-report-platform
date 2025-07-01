from simple_scraper import BookScraper

def run_all_scrapers():
    all_items = []
    book_scraper = BookScraper([
        'https://books.toscrape.com/catalogue/page-1.html',
        'https://books.toscrape.com/catalogue/page-2.html',
        'https://books.toscrape.com/catalogue/page-3.html'
    ])
    all_items.extend(book_scraper.scrape())
    return all_items

if __name__ == '__main__':
    items = run_all_scrapers()
    print(items)