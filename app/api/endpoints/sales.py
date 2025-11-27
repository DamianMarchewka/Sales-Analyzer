from fastapi import APIRouter, UploadFile, File
import pandas as pd
from io import BytesIO

router = APIRouter()

@router.post("/upload/")
async def upload_sales(file: UploadFile = File(...)):
    stats = {}
    unique = {}

    content = await file.read()
    df = pd.read_csv(BytesIO(content))

    numeric_cols = df.select_dtypes(include="number")
    for col in numeric_cols:
        stats[col] = {
            "min": float(numeric_cols[col].min()),
            "max": float(numeric_cols[col].max()),
            "mean": float(numeric_cols[col].mean()),
            "sum": float(numeric_cols[col].sum())
        }
    text_cols = df.select_dtypes(exclude="number")
    for col in text_cols:
        unique[col] = text_cols[col].astype(str).unique().tolist()
    return {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "columns_name": df.columns.tolist(),
        "numeric_stats": stats,
        "text_unique": unique
    }