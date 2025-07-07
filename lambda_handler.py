import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scraper_platform.scraper_platform.settings')

import django
django.setup()

from django.core.management import call_command


def lambda_handler(event, context):
    """
    AWS Lambda handler to run the product scraping command.
    You can pass the scraper name via event['scraper'].
    """
    scraper = event.get('scraper', 'books')
    try:
        call_command('collect_products', f'--scraper={scraper}')
        return {"status": "success", "scraper": scraper}
    except Exception as e:
        return {"status": "error", "message": str(e)}