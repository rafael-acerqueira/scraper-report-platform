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

---

## Deploying & Running Jobs on AWS Lambda

You can automate scraping tasks and run them in the cloud using AWS Lambda. This enables you to run your scraping jobs periodically, saving results directly to **any cloud PostgreSQL database** (e.g., AWS RDS, Render, Neon, Supabase, ElephantSQL, etc).

### 1. Environment Variables

**Never commit secrets!**

- Create a `.env` file at the project root (do not commit this file!)
- Define at least:
  ```
  DATABASE_URL=postgres://<USER>:<PASSWORD>@<HOST>:<PORT>/<DB_NAME>
  ```
- Use the same variable in your Lambda configuration ("Environment Variables").

### 2. Packaging the Project for Lambda

AWS Lambda requires all dependencies and code together in a ZIP file.

```bash
mkdir lambda_build
pip install --platform manylinux2014_x86_64 --target=lambda_build --implementation cp --python-version 3.10 --only-binary=:all: psycopg2-binary
pip install -r requirements.txt --target lambda_build
cp -r scraper_platform scraper lambda_handler.py lambda_build/
cp .env lambda_build/   # (or set variables in Lambda console)
cd lambda_build
zip -r ../scraper-lambda.zip .
```

**Tips:**

- Use Python 3.10 (matching the runtime selected in Lambda).
- Use `psycopg2-binary` for compatibility.
- Do not include your virtualenv folder (e.g., `.venv`, `.env`) in the ZIP.

### 3. Creating the Lambda Function

- In the AWS Console, create a new Lambda function (Python 3.10).
- Upload the `scraper-lambda.zip` file.
- Set the **Handler** to:
  ```
  lambda_handler.lambda_handler
  ```
  (This means `lambda_handler.py` file and `lambda_handler` function)
- In **Configuration > Environment Variables**, add:
  - `DATABASE_URL` with your cloud Postgres connection string.

### 4. Running the Lambda

- In the Lambda console, click **Test** and use this payload:
  ```json
  { "scraper": "books" }
  ```
- The Lambda will run the job, collect data, and save it to the database.

### 5. Accessing Your Data

- Your data will be in your configured database.
- You can access it via Django Admin, API, or your favorite SQL tool.

---

### Example Lambda Handler (lambda\_handler.py)

```python
import os
import django
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scraper_platform.scraper_platform.settings")
django.setup()

def lambda_handler(event, context):
    scraper = event.get('scraper', 'books')
    try:
        call_command('collect_products', f'--scraper={scraper}')
        return {"status": "success", "scraper": scraper}
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

---

### Notes

- **Database:** Use any managed Postgres database in the cloud: AWS RDS, Render, Neon, Supabase, ElephantSQL, etc.
- **Scheduling:** Use AWS EventBridge (CloudWatch Events) to schedule periodic Lambda invocations (e.g., every hour).
- **Security:** Use environment variables for secrets and credentials.

## License

MIT