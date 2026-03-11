from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "API working"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), email: str = Form(...)):
    try:
        # Read CSV
        df = pd.read_csv(file.file)

        # Normalize column names
        df.columns = (
            df.columns.str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        # Find columns flexibly
        revenue_col = next((c for c in df.columns if "revenue" in c), None)
        region_col = next((c for c in df.columns if "region" in c), None)
        category_col = next((c for c in df.columns if "product_category" in c or "category" in c), None)
        units_col = next((c for c in df.columns if "units" in c), None)

        if not revenue_col:
            return {"error": f"Revenue column not found. Found columns: {list(df.columns)}"}

        # Convert numbers safely
        df[revenue_col] = pd.to_numeric(df[revenue_col], errors="coerce")
        if units_col:
            df[units_col] = pd.to_numeric(df[units_col], errors="coerce")

        # Calculations
        total_revenue = df[revenue_col].sum()
        total_units = df[units_col].sum() if units_col else 0
        top_region = df.groupby(region_col)[revenue_col].sum().idxmax() if region_col else "Unknown"
        top_category = df.groupby(category_col)[revenue_col].sum().idxmax() if category_col else "Unknown"

        summary = f"""
Sales Summary Q1 2026

Total Revenue: {total_revenue}
Total Units Sold: {total_units}
Top Region: {top_region}
Top Product Category: {top_category}
"""

        return {
            "email": email,
            "summary": summary
        }

    except Exception as e:
        return {"error": str(e)}