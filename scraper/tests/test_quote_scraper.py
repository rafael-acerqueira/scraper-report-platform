from bs4 import BeautifulSoup
from scraper.quote_scraper import QuoteScraper

HTML = '''
<div class="quote">
  <span class="text">“A journey of a thousand miles begins with a single step.”</span>
  <span><small class="author">Lao Tzu</small></span>
</div>
<div class="quote">
  <span class="text">“That which does not kill us makes us stronger.”</span>
  <span><small class="author">Friedrich Nietzsche</small></span>
</div>
'''

def test_quote_scraper_parse():
    soup = BeautifulSoup(HTML, "html.parser")
    scraper = QuoteScraper(urls=[])
    quotes = scraper.parse(soup)
    assert len(quotes) == 2
    assert quotes[0]["author"] == "Lao Tzu"
    assert "single step" in quotes[0]["text"]

def test_quote_scraper_scrape(monkeypatch):
    class DummyResponse:
        def __init__(self, text):
            self.content = text.encode("utf-8")
            self.status_code = 200
        def raise_for_status(self):
            pass
    def fake_get(*args, **kwargs):
        return DummyResponse(HTML)

    import requests
    monkeypatch.setattr(requests, "get", fake_get)
    scraper = QuoteScraper(urls=["dummy"])
    result = scraper.scrape()
    assert len(result) == 2
    assert result[0]['author'] == "Lao Tzu"