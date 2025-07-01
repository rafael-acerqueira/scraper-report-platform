import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EXPORT_BUCKET_PATH = os.path.join(BASE_DIR, "s3_bucket")