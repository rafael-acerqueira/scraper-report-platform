import json
import csv
import pytest
from scraper.utils.export import export_to_json, export_to_csv

@pytest.fixture
def books_data():
    return [
        {"title": "Book A", "price": 12.34},
        {"title": "Book B", "price": 45.67}
    ]

def test_export_to_json_creates_file(tmp_path, books_data):
    export_to_json(books_data, output_dir=tmp_path, prefix="testbooks")
    files = list(tmp_path.glob("testbooks_*.json"))
    assert files, "JSON file was not created"
    file = files[0]

    with open(file, encoding="utf-8") as f:
        data = json.load(f)
    assert data == books_data

def test_export_to_csv_creates_file(tmp_path, books_data):
    export_to_csv(books_data, output_dir=tmp_path, prefix="testbooks")
    files = list(tmp_path.glob("testbooks_*.csv"))
    assert files, "CSV file was not created"
    file = files[0]

    with open(file, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert rows[0]["title"] == books_data[0]["title"]
    assert float(rows[0]["price"]) == books_data[0]["price"]
    assert len(rows) == len(books_data)
