import pytest
import random
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

@pytest.mark.django_db
def test_export_products_csv(client, admin_user):
    client.force_login(admin_user)
    Product.objects.create(title='Book 1', price='10')
    url = reverse('product-export')
    response = client.get(url + '?export_format=csv')
    assert response.status_code == 200
    assert b'title,price' in response.content  # CSV header present

@pytest.mark.django_db
def test_export_products_csv_empty(client, admin_user):
    client.force_login(admin_user)
    url = reverse('product-export')
    response = client.get(url + '?export_format=csv')
    assert response.status_code == 200

    assert b'title,price' in response.content
    assert response.content.count(b'\n') == 1

@pytest.mark.django_db
def test_export_products_json(client, admin_user):
    client.force_login(admin_user)
    Product.objects.create(title='Book 2', price='20')
    url = reverse('product-export')
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()[0]['title'] == 'Book 2'

@pytest.mark.django_db
def test_export_products_json_empty(client, admin_user):
    client.force_login(admin_user)
    url = reverse('product-export')
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.django_db
def test_export_products_json_utf8(client, admin_user):
    client.force_login(admin_user)
    Product.objects.create(title='Açaí & pão de queijo 😋', price='7.00')
    url = reverse('product-export')
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert any('Açaí & pão de queijo 😋' in item['title'] for item in data)

@pytest.mark.django_db
def test_export_products_json_with_title_filter(client, admin_user):
    client.force_login(admin_user)
    Product.objects.create(title='Django Unchained', price='40')
    Product.objects.create(title='Python for Beginners', price='25')
    url = reverse('product-export')
    response = client.get(url + '?title=Django')
    data = response.json()
    titles = [item['title'] for item in data]
    assert 'Django Unchained' in titles
    assert 'Python for Beginners' not in titles

@pytest.mark.django_db
def test_export_products_csv_multiple(client, admin_user):
    client.force_login(admin_user)
    Product.objects.create(title='Book A', price='10')
    Product.objects.create(title='Book B', price='20')
    url = reverse('product-export')
    response = client.get(url + '?export_format=csv')
    content = response.content.decode()
    assert 'Book A' in content
    assert 'Book B' in content
    assert content.count('\n') == 3

@pytest.mark.django_db
def test_export_products_csv_headers(client, admin_user):
    client.force_login(admin_user)
    Product.objects.create(title='Book Z', price='40')
    url = reverse('product-export')
    response = client.get(url + '?export_format=csv')
    assert response.status_code == 200
    assert response['Content-Type'] == 'text/csv'
    assert 'attachment' in response['Content-Disposition']

@pytest.mark.django_db
def test_export_products_csv_utf8(client, admin_user):
    client.force_login(admin_user)
    Product.objects.create(title='Coffee 🚀', price='5.50')
    url = reverse('product-export')
    response = client.get(url + '?export_format=csv')
    content = response.content.decode('utf-8')
    assert 'Coffee 🚀' in content

@pytest.mark.django_db
def test_export_products_csv_with_min_price_filter(client, admin_user):
    client.force_login(admin_user)
    Product.objects.create(title='Cheap Book', price='5')
    Product.objects.create(title='Expensive Book', price='50')
    url = reverse('product-export')
    response = client.get(url + '?export_format=csv&min_price=10')
    content = response.content.decode()
    assert 'Expensive Book' in content
    assert 'Cheap Book' not in content

@pytest.mark.django_db
def test_export_products_post_not_allowed(client, admin_user):
    client.force_login(admin_user)
    url = reverse('product-export')
    response = client.post(url, {})
    assert response.status_code == 405  # Method Not Allowed

@pytest.mark.django_db
def test_export_products_delete_not_allowed(client, admin_user):
    client.force_login(admin_user)
    url = reverse('product-export')
    response = client.delete(url)
    assert response.status_code == 405

@pytest.mark.django_db
def test_export_products_csv_many_products(client, admin_user):
    client.force_login(admin_user)
    for i in range(150):
        Product.objects.create(
            title=f'Book {i}',
            price=str(random.randint(1, 100))
        )
    url = reverse('product-export')
    response = client.get(url + '?export_format=csv')
    content = response.content.decode()

    assert content.count('\n') == 151