_SCRAPER_REGISTRY = {}

def register_scraper(name, **meta):
    """
    Scraper Registry
    ================

    This module implements a Registry pattern to centralize and organize scrapers.

    How to register a new scraper:
    -------------------------
    1. Import the decorator:
    from scraper.registry import register_scraper

    2. Decorate your class by passing a unique name:
    @register_scraper('books')
    class BookScraper(BaseScraper):
    def parse_books(self, soup):
    # parsing logic

    3. (Optional) You can add metadata:
    @register_scraper('market', description='Mercado Livre Scraper', enabled=True)
    class MercadoLivreScraper(BaseScraper):
    ...

    Access to the registry:
    -------------------
    - The registry is available as `_SCRAPER_REGISTRY`:
    from scraper.registry import _SCRAPER_REGISTRY
    print(_SCRAPER_REGISTRY.keys())

    Common errors:
    -------------
    - Duplicate names are not allowed (raises ValueError).
    - Always import the scraper module so that the decorator can run and register the class.
    """

    def decorator(cls):
        if not name or not isinstance(name, str):
            raise ValueError("Scraper name must be a non-empty string")
        if name in _SCRAPER_REGISTRY:
            raise ValueError(f"Scraper '{name}' already registered")
        _SCRAPER_REGISTRY[name] =  (cls, meta) if meta else cls
        return cls
    return decorator

def get_scraper(name):
    try:
        return _SCRAPER_REGISTRY[name]
    except KeyError:
        raise ValueError(f"Scraper '{name}' doesn't registered. Scrapers available: {available_scrapers()}")

def available_scrapers():
    return list(_SCRAPER_REGISTRY.keys())