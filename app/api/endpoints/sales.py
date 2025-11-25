from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
import pandas as pd
from io import BytesIO

router = APIRouter()

@router.post("/upload/")
async def upload_sales(file: UploadFile = File(...)):
    content = await file.read()
    df = pd.read_csv(BytesIO(content))
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "columns_name": df.columns.tolist()
    }