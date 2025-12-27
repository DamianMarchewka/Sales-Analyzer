import pandas as pd
from app.services.validate_sales import validate_csv_records
import pytest

# """
# --------------STRUCTRUE--------------
# IMPORTANT --> If structure of CSV is incorect we aborded operations
#                 we don't collect errors,
#                 we don't calculate percentages,
#                 we don't validate records,
#                 we throw ValueError as a consequence

# CONSEQUENCE --> We throw a ValueError / HTTP 400
#                 The message applies to the fila as a whole.
# """

def test_structure_validation_missing_column():
    df = pd.DataFrame([
        {"date": "2024-01-02", "product": "keyboard", "price": 10},
        {"date": "2024-01-02", "product": "mouse", "price": 5}
    ])

    with pytest.raises(ValueError):
        validate_csv_records(df, strict_threshold=1.0)


# """
# --------------STRICT THRESHOLD / ABORT--------------
# IMPORTANT --> This validation is done AFTER the records are validated.
#                 Why?
#                 We need to know the number of correct and incorrect rows,
#                 the structure is alredy OK,
#                 the data is alredy anazized.
#             If condition is False --> Abort
#                 do not return partial data.
# """

def test_validate_csv_records_validation_aborted():
    df = pd.DataFrame([
        {"date": "2024-10-02", "product": "", "quantity": 1, "price": 10},
        {"date": "01-02-2024", "product": "mouse", "quantity": 1, "price": 5},
        {"date": "2024-10-02", "product": "monitor", "quantity": 1, "price": -20},
        {"date": "2024-10-02", "product": "webcom", "quantity": 1, "price": 5}
    ])

    with pytest.raises(ValueError, match="To meny errors in records, operation aborted!"):
        validate_csv_records(df, strict_threshold=0.5)


# """
# --------------FIELD-LEVEL VALIDATION--------------
# IMPORTANT --> One invalid record doesn't corrupt whole file.
#                 We collect errors,
#                 we redord the line number,
#                 we record the details

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
