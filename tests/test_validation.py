import pandas as pd
from app.services.validate_sales import validate_csv_records
import pytest


def test_validate_csv_records_valid_input():
    df = pd.DataFrame([
        {"date": "2024-01-02", "product": "keyboard", "quantity": 1, "price": 10},
        {"date": "2024-01-02", "product": "mouse", "quantity": 1, "price": 5}
    ])
    result = validate_csv_records(df)
    assert "valid records" in result
    assert "errors" in result
    assert len(result["valid records"]) == 2
    assert len(result["errors"]) == 0


def test_validate_csv_records_error_data():
    df = pd.DataFrame([
        {"date": "01-02-2024", "product": "keyboard", "quantity": 1, "price": 10},
        {"date": "2024-01-02", "product": "mouse", "quantity": 1, "price": 5}
    ])
    result = validate_csv_records(df, strict_threshold=1.0)
    row_errors = result["errors"]
    fields = [e["field"] for err in row_errors for e in err["errors"]]
    assert "date" in fields


def test_validate_csv_records_empty_product():
    df = pd.DataFrame([
        {"date": "2024-01-02", "product": "keyboard", "quantity": 1, "price": 10},
        {"date": "2024-01-02", "product": "", "quantity": 1, "price": 5}
    ])
    result = validate_csv_records(df, strict_threshold=1.0)
    row_errors = result["errors"]
    fields = [e["field"] for err in row_errors for e in err["errors"]]
    assert "product" in fields


def test_validate_csv_records_invalid_quantity():
    df = pd.DataFrame([
        {"date": "2024-01-02", "product": "keyboard", "quantity": -2, "price": 10},
        {"date": "2024-01-02", "product": "mouse", "quantity": 1, "price": 5}
    ])
    result = validate_csv_records(df, strict_threshold=1.0)
    row_errors = result["errors"]
    fields = [e["field"] for err in row_errors for e in err["errors"]]
    assert "quantity" in fields


def test_validate_csv_records_invalid_price():
    df = pd.DataFrame([
        {"date": "2024-01-02", "product": "keyboard", "quantity": 1, "price": 10},
        {"date": "2024-01-02", "product": "mouse", "quantity": 1, "price": -5}
    ])
    result = validate_csv_records(df, strict_threshold=1.0)
    row_errors = result["errors"]
    fields = [e["field"] for err in row_errors for e in err["errors"]]
    errors_msg = [e["message"] for err in row_errors for e in err["errors"]]
    assert "price" in fields
    assert "Input should be greater than or equal to 0" in errors_msg


def test_validate_csv_records_future_date():
    df = pd.DataFrame([
        {"date": "2027-01-02", "product": "keyboard", "quantity": 1, "price": 10},
        {"date": "2024-01-02", "product": "mouse", "quantity": 1, "price": 5}
    ])

    result = validate_csv_records(df, strict_threshold=1.0)
    row_errors = result["errors"]
    errors_msg = [e["message"] for err in row_errors for e in err["errors"]]
    assert "Value error, Date form the future!" in errors_msg


def test_validate_csv_records_validation_aborted():
    df = pd.DataFrame([
        {"date": "2024-10-02", "product": "", "quantity": 1, "price": 10},
        {"date": "01-02-2024", "product": "mouse", "quantity": 1, "price": 5},
        {"date": "2024-10-02", "product": "monitor", "quantity": 1, "price": -20},
        {"date": "2024-10-02", "product": "webcom", "quantity": 1, "price": 5}
    ])

    with pytest.raises(ValueError, match="To meny errors in records, operation aborted!"):
        validate_csv_records(df, strict_threshold=0.5)


def test_validate_csv_records_missing_column():
    df = pd.DataFrame([
        {"date": "2024-01-02", "product": "keyboard", "price": 10},
        {"date": "2024-01-02", "product": "mouse", "quantity": 1, "price": 5}
    ])

    with pytest.raises(ValueError):
        validate_csv_records(df, strict_threshold=1.0)