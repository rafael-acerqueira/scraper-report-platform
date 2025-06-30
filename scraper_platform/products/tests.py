import pytest
from django.urls import reverse
from scraper_platform.products.models import Product

@pytest.mark.django_db
def test_product_list_view(client):

    Product.objects.create(title='Book A', price='R$ 10')
    Product.objects.create(title='Book B', price='R$ 20')
    Product.objects.create(title='Book C', price='R$ 30')

    url = reverse('product-list')
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert data["count"] == 3
    assert data["results"][0]["title"] == "Book C"

@pytest.mark.django_db
def test_product_detail_view(client):
    product = Product.objects.create(title='Book X', price='R$ 50')
    url = reverse('product-detail', kwargs={'pk': product.pk})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == 'Book X'
    assert data["price"] == 'R$ 50'

@pytest.mark.django_db
def test_product_filter_by_price(client):
    Product.objects.create(title='Book 1', price='R$ 10')
    Product.objects.create(title='Book 2', price='R$ 20')
    url = reverse('product-list')
    response = client.get(url, {'price': 'R$ 20'})
    assert response.status_code == 200
    data = response.json()
    assert data['count'] == 1
    assert data['results'][0]['price'] == 'R$ 20'

@pytest.mark.django_db
def test_product_filter_by_title(client):
    Product.objects.create(title='Book Alpha', price='R$ 10')
    Product.objects.create(title='Book Beta', price='R$ 20')
    Product.objects.create(title='Book Gamma', price='R$ 30')
    url = reverse('product-list')

    response = client.get(url, {'title': 'Book Alpha'})
    assert response.status_code == 200
    data = response.json()
    assert data['count'] == 1
    assert data['results'][0]['title'] == 'Book Alpha'

@pytest.mark.django_db
def test_product_pagination(client):
    for i in range(15):
        Product.objects.create(title=f'Book {i}', price=f'R$ {i*5}')
    url = reverse('product-list')
    response = client.get(url, {'page': 2, 'page_size': 10})
    assert response.status_code == 200
    data = response.json()
    assert data['count'] == 15
    assert len(data['results']) == 5
