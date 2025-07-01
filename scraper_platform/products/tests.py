import pytest
from decimal import Decimal
from django.urls import reverse
from scraper_platform.products.models import Product

@pytest.mark.django_db
def test_product_list_view(client):
    Product.objects.create(title='Book A', price=Decimal('10.00'))
    Product.objects.create(title='Book B', price=Decimal('20.00'))
    Product.objects.create(title='Book C', price=Decimal('30.00'))

    url = reverse('product-list')
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert data["count"] == 3
    assert data["results"][0]["title"] == "Book C"

@pytest.mark.django_db
def test_product_detail_view(client):
    product = Product.objects.create(title='Book X', price=Decimal('50.00'))
    url = reverse('product-detail', kwargs={'pk': product.pk})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == 'Book X'
    assert data["price"] == '50.00'

@pytest.mark.django_db
def test_product_filter_by_price(client):
    Product.objects.create(title='Book 1', price=Decimal('10.00'))
    Product.objects.create(title='Book 2', price=Decimal('20.00'))
    url = reverse('product-list')
    response = client.get(url, {'price': '20.00'})
    assert response.status_code == 200
    data = response.json()
    assert data['count'] == 1
    assert data['results'][0]['price'] == '20.00'

@pytest.mark.django_db
def test_product_filter_by_title(client):
    Product.objects.create(title='Book Alpha', price=Decimal('10.00'))
    Product.objects.create(title='Book Beta', price=Decimal('20.00'))
    Product.objects.create(title='Book Gamma', price=Decimal('30.00'))
    url = reverse('product-list')

    response = client.get(url, {'title': 'Book Alpha'})
    assert response.status_code == 200
    data = response.json()
    assert data['count'] == 1
    assert data['results'][0]['title'] == 'Book Alpha'

@pytest.mark.django_db
def test_product_pagination(client):
    for i in range(15):
        Product.objects.create(title=f'Book {i}', price=Decimal(f'{i*5:.2f}'))
    url = reverse('product-list')
    response = client.get(url, {'page': 2, 'page_size': 10})
    assert response.status_code == 200
    data = response.json()
    assert data['count'] == 15
    assert len(data['results']) == 5

@pytest.mark.django_db
def test_product_filter_min_price(client):
    Product.objects.create(title='Book A', price=Decimal('10.00'))
    Product.objects.create(title='Book B', price=Decimal('25.00'))
    Product.objects.create(title='Book C', price=Decimal('40.00'))

    url = reverse('product-list')
    response = client.get(url, {'min_price': 20})
    assert response.status_code == 200
    data = response.json()
    assert data['count'] == 2
    returned_titles = [item['title'] for item in data['results']]
    assert 'Book B' in returned_titles
    assert 'Book C' in returned_titles

@pytest.mark.django_db
def test_product_filter_max_price(client):
    Product.objects.create(title='Book A', price=Decimal('10.00'))
    Product.objects.create(title='Book B', price=Decimal('25.00'))
    Product.objects.create(title='Book C', price=Decimal('40.00'))

    url = reverse('product-list')
    response = client.get(url, {'max_price': 20})
    assert response.status_code == 200
    data = response.json()
    assert data['count'] == 1
    assert data['results'][0]['title'] == 'Book A'

@pytest.mark.django_db
def test_product_filter_title_exact(client):
    Product.objects.create(title='Unique Book', price=Decimal('15.00'))
    Product.objects.create(title='Another Book', price=Decimal('15.00'))

    url = reverse('product-list')
    response = client.get(url, {'title': 'Unique Book'})
    assert response.status_code == 200
    data = response.json()
    assert data['count'] == 1
    assert data['results'][0]['title'] == 'Unique Book'

@pytest.mark.django_db
def test_product_ordering_by_price(client):
    Product.objects.create(title='Book A', price=Decimal('30.00'))
    Product.objects.create(title='Book B', price=Decimal('10.00'))
    Product.objects.create(title='Book C', price=Decimal('20.00'))

    url = reverse('product-list')
    response = client.get(url, {'ordering': 'price'})
    assert response.status_code == 200
    data = response.json()
    prices = [float(item['price']) for item in data['results']]
    assert prices == sorted(prices)

    response_desc = client.get(url, {'ordering': '-price'})
    prices_desc = [float(item['price']) for item in response_desc.json()['results']]
    assert prices_desc == sorted(prices_desc, reverse=True)
