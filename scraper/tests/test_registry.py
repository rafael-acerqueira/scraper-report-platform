import pytest
from scraper.registry import _SCRAPER_REGISTRY, register_scraper, get_scraper

def test_register_scraper_adds_to_registry():
    class DummyScraper:
        pass

    @register_scraper('dummy')
    class DummyScraper:
        pass

    assert 'dummy' in _SCRAPER_REGISTRY
    assert _SCRAPER_REGISTRY['dummy'] is DummyScraper

def test_registry_duplicate_raises():
    _SCRAPER_REGISTRY.clear()

    @register_scraper('foo')
    class FooScraper:
        pass

    with pytest.raises(ValueError) as exc:
        @register_scraper('foo')
        class AnotherFooScraper:
            pass
    assert "already registered" in str(exc.value)

def test_registry_lists_scrapers():
    _SCRAPER_REGISTRY.clear()
    @register_scraper('a')
    class A: pass
    @register_scraper('b')
    class B: pass
    assert set(_SCRAPER_REGISTRY.keys()) == {'a', 'b'}

def test_registry_cross_module():
    from scraper.registry import register_scraper, _SCRAPER_REGISTRY
    _SCRAPER_REGISTRY.clear()


    @register_scraper('site1')
    class Site1: pass
    from scraper.registry import register_scraper as reg2
    @reg2('site2')
    class Site2: pass

    assert 'site1' in _SCRAPER_REGISTRY
    assert 'site2' in _SCRAPER_REGISTRY

def test_registry_with_custom_params():
    _SCRAPER_REGISTRY.clear()
    @register_scraper('xpto', version='1.0', enabled=True)
    class Xpto: pass

    cls, meta = _SCRAPER_REGISTRY['xpto']
    assert cls.__name__ == 'Xpto'
    assert meta['version'] == '1.0'
    assert meta['enabled'] is True

def test_registry_forbids_empty_name():
    with pytest.raises(ValueError):
        @register_scraper('')
        class Empty: pass

def test_registry_case_sensitive():
    @register_scraper('Foo')
    class Foo: pass
    @register_scraper('foo')
    class foo: pass
    assert 'Foo' in _SCRAPER_REGISTRY
    assert 'foo' in _SCRAPER_REGISTRY

def test_registry_without_params():
    _SCRAPER_REGISTRY.clear()
    @register_scraper('simple')
    class Simple: pass
    entry = _SCRAPER_REGISTRY['simple']
    if isinstance(entry, tuple):
        cls, meta = entry
        assert meta == {}
    else:
        assert entry.__name__ == 'Simple'

def test_get_scraper_returns_correct_class():
    @register_scraper('magic')
    class Magic: pass
    assert get_scraper('magic') is Magic

def test_quote_scraper_registry():
    import scraper.quote_scraper
    import importlib


    _SCRAPER_REGISTRY.clear()
    importlib.reload(scraper.quote_scraper)
    scraper_cls = get_scraper("quotes")
    assert scraper_cls is scraper.quote_scraper.QuoteScraper