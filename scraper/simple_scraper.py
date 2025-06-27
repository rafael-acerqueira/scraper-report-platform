import requests
from bs4 import BeautifulSoup

def scrape_books():
    url = 'https://books.toscrape.com/catalogue/page-1.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    books = []
    for book in soup.select('article.product_pod'):
        title = book.h3.a['title']
        price = book.select_one('.price_color').text
        books.append({'title': title, 'price': price})
    return books

if __name__ == "__main__":
    data = scrape_books()
    for item in data:
        print(item)