from fastapi import FastAPI, HTTPException
import pandas as pd
import os


app = FastAPI(
    title="Project FORESIGHT API",
    description="AI-Powered Demand & Inventory Intelligence Platform",
    version="1.0.0"
)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FORECAST_FILE = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "weekly_forecasts.csv"
)

RISK_FILE = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "inventory_risk.csv"
)


def load_forecasts():
    if not os.path.exists(FORECAST_FILE):
        raise HTTPException(
            status_code=404,
            detail="Forecast file not found. Run the pipeline first."
        )

    return pd.read_csv(FORECAST_FILE)


def load_risk():
    if not os.path.exists(RISK_FILE):
        raise HTTPException(
            status_code=404,
            detail="Inventory risk file not found. Run the pipeline first."
        )

    df = pd.read_csv(RISK_FILE)

    # Convert Snapshot_Date to datetime
    df["Snapshot_Date"] = pd.to_datetime(
        df["Snapshot_Date"],
        errors="coerce"
    )

    # Keep only the latest inventory snapshot
    latest_date = df["Snapshot_Date"].max()

    df = df[
        df["Snapshot_Date"] == latest_date
    ].copy()

    return df

@app.get("/")
def home():
    return {
        "message": "Project FORESIGHT API is running",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "Project FORESIGHT API"
    }


@app.get("/skus")
def get_skus():

    risk_df = load_risk()

    if "SKU" not in risk_df.columns:
        raise HTTPException(
            status_code=500,
            detail="SKU column not found in inventory risk data."
        )

    skus = (
        risk_df["SKU"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    return {
        "total_skus": len(skus),
        "skus": skus
    }


@app.get("/forecast/{sku}")
def get_forecast(sku: str):

    forecast_df = load_forecasts()

    if "SKU" not in forecast_df.columns:
        raise HTTPException(
            status_code=500,
            detail="SKU column not found in forecast data."
        )

    result = forecast_df[
        forecast_df["SKU"].astype(str) == str(sku)
    ]

    if result.empty:
        raise HTTPException(
            status_code=404,
            detail=f"No forecast found for SKU {sku}"
        )

    return result.to_dict(orient="records")


@app.get("/inventory/{sku}")
def get_inventory(sku: str):

    risk_df = load_risk()

    result = risk_df[
        risk_df["SKU"].astype(str) == str(sku)
    ]

    if result.empty:
        raise HTTPException(
            status_code=404,
            detail=f"No inventory information found for SKU {sku}"
        )

    row = result.iloc[0]

    response = {}

    for column in result.columns:

        value = row[column]

        if pd.isna(value):
            response[column] = None

        elif hasattr(value, "item"):
            response[column] = value.item()

        else:
            response[column] = value

    return response


@app.get("/risk/{sku}")
def get_risk(sku: str):

    risk_df = load_risk()

    result = risk_df[
        risk_df["SKU"].astype(str) == str(sku)
    ]

    if result.empty:
        raise HTTPException(
            status_code=404,
            detail=f"No risk information found for SKU {sku}"
        )

    row = result.iloc[0]

    return {
        "SKU": str(row["SKU"]),
        "Stockout_Risk": str(row["Stockout_Risk"]),
        "Overstock_Risk": str(row["Overstock_Risk"]),
        "Overall_Risk": str(row["Overall_Risk"]),
        "Risk_Score": int(row["Risk_Score"]),
        "Recommendation": str(row["Recommendation"])
    }


@app.get("/recommendations")
def get_recommendations():

    risk_df = load_risk()

    if "Recommendation" not in risk_df.columns:
        raise HTTPException(
            status_code=500,
            detail="Recommendation column not found."
        )

    result = risk_df[
    [
        "SKU",
        "Stockout_Risk",
        "Overstock_Risk",
        "Overall_Risk",
        "Risk_Score",
        "Recommendation"
    ]
].copy()

    result["SKU"] = result["SKU"].astype(str)
    result["Overall_Risk"] = result["Overall_Risk"].astype(str)
    result["Stockout_Risk"] = result["Stockout_Risk"].astype(str)
    result["Overstock_Risk"] = result["Overstock_Risk"].astype(str)
    result["Risk_Score"] = result["Risk_Score"].astype(int)
    result["Recommendation"] = result["Recommendation"].astype(str)

    return result.to_dict(orient="records")


@app.get("/risk-summary")
def risk_summary():

    risk_df = load_risk()

    total_skus = risk_df["SKU"].nunique()

    high_risk = len(
        risk_df[
            risk_df["Overall_Risk"] == "HIGH"
        ]
    )

    stockout_risk = len(
        risk_df[
            risk_df["Stockout_Risk"] == "HIGH"
        ]
    )

    overstock_risk = len(
        risk_df[
            risk_df["Overstock_Risk"] == "HIGH"
        ]
    )

    reorder_now = len(
        risk_df[
            risk_df["Recommendation"] == "REORDER NOW"
        ]
    )

    reorder_soon = len(
        risk_df[
            risk_df["Recommendation"] == "REORDER SOON"
        ]
    )

    markdown_clear = len(
        risk_df[
            risk_df["Recommendation"] == "MARKDOWN / CLEAR"
        ]
    )

    healthy = len(
        risk_df[
            risk_df["Recommendation"] == "HEALTHY"
        ]
    )

    return {
        "total_skus": int(total_skus),
        "high_risk": int(high_risk),
        "stockout_risk": int(stockout_risk),
        "overstock_risk": int(overstock_risk),
        "reorder_now": int(reorder_now),
        "reorder_soon": int(reorder_soon),
        "markdown_clear": int(markdown_clear),
        "healthy": int(healthy)
    }