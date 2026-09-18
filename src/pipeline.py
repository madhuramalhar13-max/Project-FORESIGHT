import pandas as pd

from src.features import (
    prepare_weekly_demand,
    build_lag_and_rolling_features
)

from src.forecast import (
    train_lgbm,
    generate_future_forecast
)

from src.risk import calculate_inventory_risk


SALES_FILE = "data/processed/processed_sales.csv"
CALENDAR_FILE = "data/processed/processed_calendar.csv"
INVENTORY_FILE = "data/processed/processed_inventory.csv"

FUTURE_FORECAST_FILE = "data/processed/future_forecasts.csv"
RISK_OUTPUT_FILE = "data/processed/inventory_risk.csv"


def run_pipeline():

    print("=" * 50)
    print("PROJECT FORESIGHT PIPELINE")
    print("=" * 50)

    print("\nLoading historical sales data...")
    sales_df = pd.read_csv(SALES_FILE)
    print(f"Sales records loaded: {len(sales_df)}")

    print("Loading calendar data...")
    calendar_df = pd.read_csv(CALENDAR_FILE)
    print(f"Calendar records loaded: {len(calendar_df)}")

    print("\nPreparing weekly demand...")
    weekly_df = prepare_weekly_demand(
        sales_df,
        calendar_df
    )
    print(f"Weekly records created: {len(weekly_df)}")

    print("\nBuilding forecasting features...")
    feature_df = build_lag_and_rolling_features(
        weekly_df
    )

    model_df = feature_df.dropna().copy()
    print(f"Training records available: {len(model_df)}")

    print("\nTraining LightGBM model...")
    model = train_lgbm(model_df)
    print("LightGBM training completed.")

    print("\nGenerating 12-week future forecast...")

    future_forecast_df = generate_future_forecast(
        model,
        weekly_df,
        weeks_ahead=12
    )

    future_forecast_df.to_csv(
        FUTURE_FORECAST_FILE,
        index=False
    )

    print("\nFuture forecast file created:")
    print(FUTURE_FORECAST_FILE)

    print(
        f"Future forecast records: "
        f"{len(future_forecast_df)}"
    )

    print("\nLoading inventory data...")
    inventory_df = pd.read_csv(INVENTORY_FILE)
    print(f"Inventory records loaded: {len(inventory_df)}")

    print("\nCalculating inventory risks...")

    risk_df = calculate_inventory_risk(
        future_forecast_df,
        inventory_df
    )

    risk_df.to_csv(
        RISK_OUTPUT_FILE,
        index=False
    )

    print("\nInventory risk file created:")
    print(RISK_OUTPUT_FILE)

    print("\n" + "=" * 50)
    print("INVENTORY RISK SUMMARY")
    print("=" * 50)

    risk_df["Snapshot_Date"] = pd.to_datetime(
        risk_df["Snapshot_Date"],
        errors="coerce"
    )

    latest_date = risk_df["Snapshot_Date"].max()

    summary_df = risk_df[
        risk_df["Snapshot_Date"] == latest_date
    ].copy()

    total_skus = summary_df["SKU"].nunique()

    high_risk = len(
        summary_df[
            summary_df["Overall_Risk"] == "HIGH"
        ]
    )

    stockout_risk = len(
        summary_df[
            summary_df["Stockout_Risk"] == "HIGH"
        ]
    )

    overstock_risk = len(
        summary_df[
            summary_df["Overstock_Risk"] == "HIGH"
        ]
    )

    reorder_now = len(
        summary_df[
            summary_df["Recommendation"] == "REORDER NOW"
        ]
    )

    reorder_soon = len(
        summary_df[
            summary_df["Recommendation"] == "REORDER SOON"
        ]
    )

    markdown_clear = len(
        summary_df[
            summary_df["Recommendation"] == "MARKDOWN / CLEAR"
        ]
    )

    healthy = len(
        summary_df[
            summary_df["Recommendation"] == "HEALTHY"
        ]
    )

    print(f"Total SKUs:       {total_skus}")
    print(f"High Risk:        {high_risk}")
    print(f"Stockout Risk:    {stockout_risk}")
    print(f"Overstock Risk:   {overstock_risk}")
    print(f"Reorder Now:      {reorder_now}")
    print(f"Reorder Soon:     {reorder_soon}")
    print(f"Markdown/Clear:   {markdown_clear}")
    print(f"Healthy:          {healthy}")

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()
