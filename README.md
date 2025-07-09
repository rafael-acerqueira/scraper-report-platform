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

## Environment Variables

You must configure some environment variables to run the project both locally and in production (AWS Lambda):

**Database (required):**

- `DATABASE_URL` – PostgreSQL connection string (for example, from Neon, Supabase, AWS RDS, etc.)

**AWS S3 Export (optional, but recommended for production):**

- `S3_BUCKET` (or `AWS_STORAGE_BUCKET_NAME`) – Name of your S3 bucket.
- `AWS_DEFAULT_REGION` – AWS region (e.g., `us-east-1`).
- `AWS_ACCESS_KEY_ID` – (required locally or if Lambda Role does not have S3 access)
- `AWS_SECRET_ACCESS_KEY` – (required locally or if Lambda Role does not have S3 access)
- `S3_PREFIX` – (optional) Subfolder within your bucket for reports.

> **Tip:**\
> On AWS Lambda, if your Lambda function has a Role with S3 permissions, you may omit `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.\
> For local development, you must provide these credentials in your `.env` file or via `aws configure`.

Example `.env` for local development:

```env
DATABASE_URL=postgres://myuser:mypass@myhost:5432/mydb
S3_BUCKET=my-scraper-bucket
AWS_DEFAULT_REGION=us-east-1
AWS_ACCESS_KEY_ID=xxxxxxxxxxxx
AWS_SECRET_ACCESS_KEY=yyyyyyyyyyyyyyyyyy
S3_PREFIX=reports
```

---

## Roadmap

- [x] Initial project and repository setup
- [x] Virtual environment and Django setup
- [x] Modular scraping engine (BeautifulSoup)
- [x] Django Product model, API (list, retrieve, filter, paginate)
- [x] Export functionality: JSON & CSV
- [x] Pytest: API and scraper tests
- [x] CI/CD pipeline with GitHub Actions
- [x] Best practices for Django project layout
- [x] Marketplace scraping implementation (multi-site)
- [x] Store/export reports to AWS S3
- [ ] Task automation with AWS Lambda
- [x] Authentication and advanced filtering
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

### Exporting to S3 (AWS)

To automatically export your CSV and JSON reports directly to **AWS S3** (instead of a local folder), configure these environment variables in your Lambda function, Docker container, or production server:

```env
S3_BUCKET=your-bucket-name
S3_PREFIX=your/subfolder/path  # (optional, can be left blank)
```

- `S3_BUCKET` (**required**): Name of the S3 bucket where exports will be saved.
- `S3_PREFIX` (optional): Subfolder within the bucket. If not set, files go to the bucket root.

**How it works:**

- When these variables are present, the export functions will upload files directly to S3.
- If not set, files are saved locally to the default folder (e.g., `s3_bucket/`).

**Example for AWS Lambda:**

- Go to your Lambda console, under **Configuration → Environment variables**.
- Add:
  - `S3_BUCKET = my-company-data`
  - `S3_PREFIX = reports` (or leave blank for the root)

Now, every export will go straight to S3, ready for use in BI, reporting, or further automations.

---

### Notes

- **Database:** Use any managed Postgres database in the cloud: AWS RDS, Render, Neon, Supabase, ElephantSQL, etc.
- **Scheduling:** Use AWS EventBridge (CloudWatch Events) to schedule periodic Lambda invocations (e.g., every hour).
- **Security:** Use environment variables for secrets and credentials.

## License

MIT