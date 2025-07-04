import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EXPORT_BUCKET_PATH = os.path.join(BASE_DIR, "s3_bucket")

ADMIN_SITE_HEADER = "Scraper Report Platform Admin"
ADMIN_SITE_TITLE = "Scraper Admin"
ADMIN_INDEX_TITLE = "Welcome to Scraper Painel"