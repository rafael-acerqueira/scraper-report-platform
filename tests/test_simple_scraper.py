from scraper.simple_scraper import scrape_books

def test_scrape_books():
    books = scrape_books()
    assert isinstance(books, list)
    assert len(books) > 0
    assert 'title' in books[0]
    assert 'price' in books[0]