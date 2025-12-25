import pandas as pd
from app.services.validate_sales import validate_csv_records
import pytest

# """
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