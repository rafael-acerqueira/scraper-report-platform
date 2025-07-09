import os
import json
import csv
from datetime import datetime

def is_lambda_env():
    """Detect if running in AWS Lambda or USE_S3_EXPORT is set."""
    return (
        os.environ.get("AWS_EXECUTION_ENV") or
        os.environ.get("USE_S3_EXPORT") == "1"
    )

def get_export_dir():
    """Return local dir or s3 path depending on environment/settings."""

    s3_bucket = os.environ.get("S3_BUCKET")
    if s3_bucket:
        s3_prefix = os.environ.get("S3_PREFIX", "").strip("/")
        if s3_prefix:
            return f"s3://{s3_bucket}/{s3_prefix}"
        else:
            return f"s3://{s3_bucket}"

    from django.conf import settings
    return getattr(settings, "EXPORT_BUCKET_PATH", "s3_bucket")

def export_to_json(data, output_dir=None, prefix='books'):
    export_dir = output_dir or get_export_dir()
    filename = f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    if export_dir.startswith("s3://"):
        _export_to_s3(json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"), export_dir, filename, "application/json")
        print(f"Exported {len(data)} records to {export_dir}/{filename} (S3)")
    else:
        os.makedirs(export_dir, exist_ok=True)
        path = os.path.join(export_dir, filename)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Exported {len(data)} records to {path}")

def export_to_csv(data, output_dir=None, prefix='books'):
    export_dir = output_dir or get_export_dir()
    filename = f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    if export_dir.startswith("s3://"):
        import io
        output = io.StringIO()
        if data:
            writer = csv.DictWriter(output, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
            csv_bytes = output.getvalue().encode("utf-8")
        else:
            csv_bytes = b"No data\n"
        _export_to_s3(csv_bytes, export_dir, filename, "text/csv")
        print(f"Exported {len(data)} records to {export_dir}/{filename} (S3)")
    else:
        os.makedirs(export_dir, exist_ok=True)
        path = os.path.join(export_dir, filename)
        if data:
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            print(f"Exported {len(data)} records to {path}")
        else:
            print("No data to export.")

def _export_to_s3(data_bytes, s3_dir, filename, content_type):
    import boto3
    assert s3_dir.startswith("s3://")
    _, _, rest = s3_dir.partition("s3://")
    if "/" in rest:
        bucket, prefix = rest.split("/", 1)
        s3_key = f"{prefix.rstrip('/')}/{filename}"
    else:
        bucket = rest
        s3_key = filename
    s3 = boto3.client("s3")
    s3.put_object(Bucket=bucket, Key=s3_key, Body=data_bytes, ContentType=content_type)