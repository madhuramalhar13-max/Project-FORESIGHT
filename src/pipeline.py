from src.risk import calculate_inventory_risk, generate_risk_summary
from pathlib import Path

import pandas as pd

from src.features import (
    prepare_weekly_demand,
    build_lag_and_rolling_features
)

from src.baseline import SeasonalNaiveBaseline

from src.forecast import train_lgbm, FEATURES

from src.metrics import calculate_wape

from src.risk import (
    calculate_inventory_risk,
    generate_risk_summary
)


# =========================================================
# PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

SALES_FILE = (
    BASE_DIR /
    "data" /
    "processed" /
    "processed_sales.csv"
)

CALENDAR_FILE = (
    BASE_DIR /
    "data" /
    "processed" /
    "processed_calendar.csv"
)

INVENTORY_FILE = (
    BASE_DIR /
    "data" /
    "processed" /
    "processed_inventory.csv"
)

FORECAST_FILE = (
    BASE_DIR /
    "data" /
    "processed" /
    "weekly_forecasts.csv"
)

RISK_FILE = (
    BASE_DIR /
    "data" /
    "processed" /
    "inventory_risk.csv"
)


# =========================================================
# LOAD DATA
# =========================================================

def load_data():

    print("\nLoading data...")

    sales = pd.read_csv(SALES_FILE)

    calendar = pd.read_csv(CALENDAR_FILE)

    inventory = pd.read_csv(INVENTORY_FILE)

    print(f"Sales rows:     {len(sales)}")
    print(f"Calendar rows:  {len(calendar)}")
    print(f"Inventory rows: {len(inventory)}")

    return sales, calendar, inventory


# =========================================================
# PREPARE FEATURES
# =========================================================

def prepare_data(sales, calendar):

    print("\nPreparing weekly demand...")

    weekly_data = prepare_weekly_demand(
        sales,
        calendar
    )

    print(
        f"Weekly demand rows: {len(weekly_data)}"
    )

    print("\nBuilding lag and rolling features...")

    feature_data = build_lag_and_rolling_features(
        weekly_data
    )

    return feature_data


# =========================================================
# CLEAN DATA
# =========================================================

def clean_data(feature_data):

    print("\nCleaning model data...")

    required_columns = FEATURES + [
        "Units_Sold"
    ]

    before = len(feature_data)

    model_data = feature_data.dropna(
        subset=required_columns
    ).copy()

    after = len(model_data)

    print(f"Rows before cleaning: {before}")
    print(f"Rows after cleaning:  {after}")
    print(f"Rows removed:         {before - after}")

    return model_data


# =========================================================
# TRAIN / TEST SPLIT
# =========================================================

def split_data(model_data):

    print("\nCreating time-based train/test split...")

    dates = sorted(
        model_data["Week_Start"].unique()
    )

    split_index = int(
        len(dates) * 0.80
    )

    split_date = dates[split_index]

    train_data = model_data[
        model_data["Week_Start"] < split_date
    ].copy()

    test_data = model_data[
        model_data["Week_Start"] >= split_date
    ].copy()

    print(
        f"Training rows: {len(train_data)}"
    )

    print(
        f"Testing rows:  {len(test_data)}"
    )

    return train_data, test_data


# =========================================================
# TRAIN LIGHTGBM
# =========================================================

def train_model(train_data):

    print("\nTraining LightGBM...")

    model = train_lgbm(
        train_data
    )

    print(
        "LightGBM training completed."
    )

    return model


# =========================================================
# GENERATE LIGHTGBM FORECAST
# =========================================================

def generate_predictions(
    model,
    test_data
):

    print(
        "\nGenerating LightGBM predictions..."
    )

    predictions = model.predict(
        test_data[FEATURES]
    )

    predictions = pd.Series(
        predictions,
        index=test_data.index
    )

    return predictions


# =========================================================
# GENERATE BASELINE
# =========================================================

def generate_baseline_predictions(
    test_data
):

    print(
        "\nGenerating Seasonal Naive predictions..."
    )

    baseline = SeasonalNaiveBaseline(
        seasonality=52
    )

    predictions = baseline.predict(
        test_data
    )

    return predictions


# =========================================================
# MODEL EVALUATION
# =========================================================

def evaluate_models(
    test_data,
    lgbm_predictions,
    baseline_predictions
):

    actual = test_data[
        "Units_Sold"
    ]

    lgbm_wape = calculate_wape(
        actual,
        lgbm_predictions
    )

    baseline_wape = calculate_wape(
        actual,
        baseline_predictions
    )

    print("\n==============================")
    print("MODEL EVALUATION")
    print("==============================")

    print(
        f"Seasonal Naive WAPE : "
        f"{baseline_wape:.4f}"
    )

    print(
        f"LightGBM WAPE       : "
        f"{lgbm_wape:.4f}"
    )

    print("==============================")

    return baseline_wape, lgbm_wape


# =========================================================
# SAVE FORECASTS
# =========================================================

def save_forecasts(
    test_data,
    predictions
):

    print("\nSaving forecasts...")

    output = test_data[
        [
            "Week_Start",
            "SKU",
            "Units_Sold"
        ]
    ].copy()

    output[
        "Forecast_Units"
    ] = predictions

    output = output.sort_values(
        [
            "SKU",
            "Week_Start"
        ]
    )

    output.to_csv(
        FORECAST_FILE,
        index=False
    )

    print(
        f"Forecast saved to:\n"
        f"{FORECAST_FILE}"
    )

    return output


# =========================================================
# INVENTORY RISK ANALYSIS
# =========================================================

def run_risk_engine(
    inventory,
    forecast
):

    print("\n")
    print("==============================")
    print("INVENTORY RISK ANALYSIS")
    print("==============================")

    risk_result = calculate_inventory_risk(
        inventory,
        forecast
    )

    risk_result.to_csv(
        RISK_FILE,
        index=False
    )

    summary = generate_risk_summary(
        risk_result
    )

    print(
        f"\nTotal SKUs:       "
        f"{summary['total_skus']}"
    )

    print(
        f"High Risk:        "
        f"{summary['high_risk']}"
    )

    print(
        f"Stockout Risk:    "
        f"{summary['stockout_risk']}"
    )

    print(
        f"Overstock Risk:   "
        f"{summary['overstock_risk']}"
    )

    print(
        f"Reorder Now:      "
        f"{summary['reorder_now']}"
    )

    print(
        f"Reorder Soon:     "
        f"{summary['reorder_soon']}"
    )

    print(
        f"Markdown/Clear:   "
        f"{summary['markdown_clear']}"
    )

    print(
        f"Healthy:          "
        f"{summary['healthy']}"
    )

    print(
        f"\nRisk report saved to:\n"
        f"{RISK_FILE}"
    )

    return risk_result


# =========================================================
# MAIN
# =========================================================

def main():

    print("\n")
    print("==========================================")
    print("        PROJECT FORESIGHT")
    print("  DEMAND & INVENTORY INTELLIGENCE")
    print("==========================================")

    # -----------------------------------------------------
    # 1. LOAD DATA
    # -----------------------------------------------------

    sales, calendar, inventory = load_data()

    # -----------------------------------------------------
    # 2. FEATURE ENGINEERING
    # -----------------------------------------------------

    feature_data = prepare_data(
        sales,
        calendar
    )

    # -----------------------------------------------------
    # 3. CLEAN DATA
    # -----------------------------------------------------

    model_data = clean_data(
        feature_data
    )

    # -----------------------------------------------------
    # 4. TRAIN / TEST SPLIT
    # -----------------------------------------------------

    train_data, test_data = split_data(
        model_data
    )

    # -----------------------------------------------------
    # 5. TRAIN MODEL
    # -----------------------------------------------------

    model = train_model(
        train_data
    )

    # -----------------------------------------------------
    # 6. LIGHTGBM FORECAST
    # -----------------------------------------------------

    lgbm_predictions = generate_predictions(
        model,
        test_data
    )

    # -----------------------------------------------------
    # 7. BASELINE FORECAST
    # -----------------------------------------------------

    baseline_predictions = (
        generate_baseline_predictions(
            test_data
        )
    )

    # -----------------------------------------------------
    # 8. EVALUATE
    # -----------------------------------------------------

    baseline_wape, lgbm_wape = (
        evaluate_models(
            test_data,
            lgbm_predictions,
            baseline_predictions
        )
    )

    # -----------------------------------------------------
    # 9. SAVE FORECAST
    # -----------------------------------------------------

    forecast = save_forecasts(
        test_data,
        lgbm_predictions
    )

    # -----------------------------------------------------
    # 10. RUN RISK ENGINE
    # -----------------------------------------------------

    risk_result = run_risk_engine(
        inventory,
        forecast
    )

    # -----------------------------------------------------
    # 11. FINAL OUTPUT
    # -----------------------------------------------------

    print("\n")
    print("==========================================")
    print("        FORESIGHT PIPELINE COMPLETE")
    print("==========================================")

    print(
        f"\nBaseline WAPE : "
        f"{baseline_wape:.4f}"
    )

    print(
        f"LightGBM WAPE : "
        f"{lgbm_wape:.4f}"
    )

    print(
        f"Risk records  : "
        f"{len(risk_result)}"
    )

    print("\nGenerated files:")

    print(
        "1. data/processed/weekly_forecasts.csv"
    )

    print(
        "2. data/processed/inventory_risk.csv"
    )


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    main()