import os
import json
import csv
from datetime import datetime
from django.conf import settings


def get_export_dir():
    try:
        return getattr(settings, "EXPORT_BUCKET_PATH", "s3_bucket")
    except Exception:
        return "s3_bucket"

def export_to_json(data, output_dir=None, prefix='books'):
    if output_dir is None:
        output_dir = get_export_dir()
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    path = os.path.join(output_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Exported {len(data)} records to {path}")

def export_to_csv(data, output_dir=None, prefix='books'):
    if output_dir is None:
        output_dir = get_export_dir()
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    path = os.path.join(output_dir, filename)
    if data:
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        print(f"Exported {len(data)} records to {path}")
    else:
        print("No data to export.")