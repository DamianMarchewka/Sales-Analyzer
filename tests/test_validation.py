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