# Scraper Report Platform
[![Django CI](https://github.com/rafael-acerqueira/scraper-report-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/rafael-acerqueira/scraper-report-platform/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue?logo=python)
![Django](https://img.shields.io/badge/django-5%2B-darkgreen?logo=django)
![License](https://img.shields.io/github/license/rafael-acerqueira/scraper-report-platform)


&#x20; &#x20;

## Description

Scraper Report Platform is a robust and modular data collection and reporting system. Built with Django, Django REST Framework, and BeautifulSoup, the platform enables scraping of marketplace or e-commerce data, structured storage, and robust API access.\
The project is designed for extensibility (adding new sites or scrapers is easy), professional workflow, and real-world applicability.

## Tech Stack

- Python 3.10+
- Django 5+
- Django REST Framework
- BeautifulSoup (scraping engine)
- Pytest (unit & integration testing)
- SQLite (development)
- GitHub Actions (CI/CD)
- (Soon: AWS S3 for reports, AWS Lambda for automation)

## Key Features Implemented

- Modular project structure (Django + scripts)
- Reusable scraping module using BeautifulSoup
- Export scraped data as JSON and CSV
- Store, list, and filter products in the Django database
- Paginated, filterable API for products
- Test suite with Pytest for both scraper and API
- GitHub Actions workflow for continuous integration
- Project now follows best practices for Django package organization (manage.py at root, apps importable, no hacks needed)

## Project Structure

```
scraper-report-platform/
├── manage.py
├── scraper_platform/         # Django project and apps
│   ├── scraper_platform/     # Django settings, urls, wsgi
│   └── products/             # Django app: products, API, tests
├── scraper/                  # Standalone scraping module
├── requirements.txt
├── .gitignore
└── README.md
```

## Roadmap

- [x] Initial project and repository setup
- [x] Virtual environment and Django setup
- [x] Modular scraping engine (BeautifulSoup)
- [x] Django Product model, API (list, retrieve, filter, paginate)
- [x] Export functionality: JSON & CSV
- [x] Pytest: API and scraper tests
- [x] CI/CD pipeline with GitHub Actions
- [x] Best practices for Django project layout
- [ ] Marketplace scraping implementation (multi-site)
- [ ] Store/export reports to AWS S3
- [ ] Task automation with AWS Lambda
- [ ] Authentication and advanced filtering
- [ ] Final documentation and presentation

## How to run locally

```bash
# Clone the repository
git clone https://github.com/yourusername/scraper-report-platform.git
cd scraper-report-platform

# Create and activate a virtual environment
python -m venv .env
source .env/bin/activate  # Linux/macOS
.env\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run Django migrations
python manage.py migrate

# Run tests (optional)
pytest

# Start the Django server
python manage.py runserver
```

## License

MIT
