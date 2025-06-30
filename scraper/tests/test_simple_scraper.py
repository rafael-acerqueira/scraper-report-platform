import os
import json
import csv
import glob

from scraper.simple_scraper import export_to_json, export_to_csv

TEST_OUTPUT_DIR = "scraper/outputs"
DUMMY_DATA = [
    {'title': 'Book 1', 'price': '£10.00'},
    {'title': 'Book 2', 'price': '£20.00'},
]

def cleanup_files(pattern):
    for file_path in glob.glob(pattern):
        os.remove(file_path)

def test_export_to_json():
    cleanup_files(f"{TEST_OUTPUT_DIR}/testbooks_*.json")
    export_to_json(DUMMY_DATA, output_dir=TEST_OUTPUT_DIR, prefix='testbooks')
    files = glob.glob(f"{TEST_OUTPUT_DIR}/testbooks_*.json")
    assert files, "No JSON file generated."
    with open(files[0], 'r', encoding='utf-8') as f:
        data = json.load(f)
    assert data == DUMMY_DATA
    cleanup_files(f"{TEST_OUTPUT_DIR}/testbooks_*.json")

def test_export_to_csv():
    cleanup_files(f"{TEST_OUTPUT_DIR}/testbooks_*.csv")
    export_to_csv(DUMMY_DATA, output_dir=TEST_OUTPUT_DIR, prefix='testbooks')
    files = glob.glob(f"{TEST_OUTPUT_DIR}/testbooks_*.csv")
    assert files, "No CSV file generated."
    with open(files[0], newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert rows[0]['title'] == DUMMY_DATA[0]['title']
    assert rows[0]['price'] == DUMMY_DATA[0]['price']
    assert len(rows) == 2
    cleanup_files(f"{TEST_OUTPUT_DIR}/testbooks_*.csv")