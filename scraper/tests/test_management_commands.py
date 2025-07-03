import pytest
from django.core.management import call_command
from io import StringIO
from scraper.registry import _SCRAPER_REGISTRY, register_scraper

@pytest.mark.django_db
def test_list_scrapers_command_output():
    _SCRAPER_REGISTRY.clear()
    @register_scraper('testsite')
    class Dummy: pass

    out = StringIO()
    call_command('list_scrapers', stdout=out)
    output = out.getvalue()
    assert "testsite" in output