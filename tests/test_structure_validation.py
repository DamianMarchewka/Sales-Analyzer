import pandas as pd
from app.services.validate_sales import validate_csv_records
import pytest

# """
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