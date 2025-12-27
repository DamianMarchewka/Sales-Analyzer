from app.models.schemas import SalesInput
from pydantic import ValidationError
import pandas as pd

def validate_csv_records(df: pd.DataFrame, row_offset: int=1, strict_threshold: float=0.1):
    """
    Validate all CSV records using the SalesInput model.
    df: pandas DataFrame with CSV content
    row_offset: offset for row numbering (1 if CSV has a header)
    strict_threshold: allowed percentage of invalid rows
    """

    required = {"date", "product", "quantity", "price"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    
    records = df.to_dict(orient="records")

    valid_records = []
    errors = []

    for idx, rec in enumerate(records, start=row_offset):
        try:
            validated = SalesInput(**rec) # type: ignore
            valid_records.append(validated.model_dump())
        except ValidationError as e:
            errors.append({
                "row": idx,
                "raw": rec,
                "error": e.errors()
            })

    total = len(records)
    bad_count = len(errors)
    errors_rate = bad_count / total

    if errors_rate > strict_threshold:
        raise ValueError("To meny errors in records, operation aborted!")

    simplified_errors = []
    for err in errors:
        simplified_errors_for_row = []
        for e in err["error"]:
            if len(e["loc"]) > 0:
                field = e["loc"][0]
            else:
                field = "model"
            simplified_errors_for_row.append({
                "field": field,
                "message": e["msg"]
            })
        simplified_errors.append({
            "row": err["row"],
            "errors": simplified_errors_for_row
            })
    return {
        "valid records": valid_records,
        "errors": simplified_errors
    }
