import pandas as pd
from app.services.validate_sales import validate_csv_records

def test_validate_csv_records_valid_input():
    df = pd.DataFrame([
        {"date": "2024-01-02", "product": "keyboard", "quantity": 1, "price": 10},
        {"date": "2024-01-02", "product": "mouse", "quantity": 1, "price": 5},
    ])
    result = validate_csv_records(df)

    assert "valid records" in result
    assert "errors" in result
    assert len(result["valid records"]) == 2
    assert len(result["errors"]) == 0

def test_validate_csv_records_error_data():
    df = pd.DataFrame([
        {"date": "01-02-2024", "product": "keyboard", "quantity": 1, "price": 10},
        {"date": "2024-01-02", "product": "", "quantity": 1, "price": 5},
        {"date": "2024-04-11", "product": "monitor", "quantity": 2, "price": -25},
        {"date": "2026-06-04", "product": "webcam", "quantity": 1, "price": 15},
        {"date": "2024-02-14", "product": "monitor", "quantity": 1, "price": 205}
    ])
    result = validate_csv_records(df, strict_threshold=1.0)

    assert "valid records" in result
    assert "errors" in result
    assert len(result["valid records"]) == 1
    assert len(result["errors"]) == 4
    row_errors = result["errors"]
    fields = [e["field"] for err in row_errors for e in err["errors"]]