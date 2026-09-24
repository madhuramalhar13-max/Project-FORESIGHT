import pandas as pd
import numpy as np


# ---------------------------------------------------------
# CALCULATE INVENTORY RISK
# ---------------------------------------------------------

def calculate_inventory_risk(inventory_df, forecast_df):

    inventory = inventory_df.copy()
    forecast = forecast_df.copy()

    # -----------------------------------------------------
    # CLEAN COLUMN NAMES
    # -----------------------------------------------------

    inventory.columns = inventory.columns.str.strip()
    forecast.columns = forecast.columns.str.strip()

    # -----------------------------------------------------
    # PREPARE FORECAST DATA
    # -----------------------------------------------------

    forecast_summary = (
        forecast
        .groupby("SKU")["Forecast_Units"]
        .mean()
        .reset_index()
    )

    forecast_summary.rename(
        columns={
            "Forecast_Units": "Average_Forecast_Demand"
        },
        inplace=True
    )

    # -----------------------------------------------------
    # MERGE INVENTORY + FORECAST
    # -----------------------------------------------------

    result = inventory.merge(
        forecast_summary,
        on="SKU",
        how="left"
    )

    # If a SKU has no forecast, assume zero forecast
    result["Average_Forecast_Demand"] = (
        result["Average_Forecast_Demand"]
        .fillna(0)
    )

    # -----------------------------------------------------
    # AVOID DIVISION BY ZERO
    # -----------------------------------------------------

    result["Average_Forecast_Demand"] = (
        result["Average_Forecast_Demand"].replace(0, np.nan)
    )

    # -----------------------------------------------------
    # STOCK COVERAGE
    # -----------------------------------------------------

    result["Stock_Coverage_Weeks"] = (
        result["Current_Stock"] /
        result["Average_Forecast_Demand"]
    )

    result["Stock_Coverage_Weeks"] = (
        result["Stock_Coverage_Weeks"]
        .replace([np.inf, -np.inf], np.nan)
        .fillna(0)
    )

    # -----------------------------------------------------
    # EXPECTED DEMAND DURING LEAD TIME
    # -----------------------------------------------------

    result["Lead_Time_Weeks"] = (
        result["Lead_Time_Days"] / 7
    )

    result["Lead_Time_Demand"] = (
        result["Average_Forecast_Demand"] *
        result["Lead_Time_Weeks"]
    )

    # -----------------------------------------------------
    # AVAILABLE STOCK
    # -----------------------------------------------------

    result["Available_Stock"] = (
        result["Current_Stock"] +
        result["On_Order"]
    )

    # -----------------------------------------------------
    # STOCKOUT RISK
    # -----------------------------------------------------

    result["Stockout_Gap"] = (
        result["Lead_Time_Demand"] +
        result["Safety_Stock"] -
        result["Available_Stock"]
    )

    result["Stockout_Risk"] = np.where(
        result["Stockout_Gap"] > 0,
        "HIGH",
        "LOW"
    )

    # -----------------------------------------------------
    # OVERSTOCK RISK
    # -----------------------------------------------------

    # Three months of demand is used as an inventory
    # reference point for identifying possible overstock.

    target_inventory = (
        result["Average_Forecast_Demand"] * 12
    )

    result["Excess_Stock"] = (
        result["Current_Stock"] -
        target_inventory
    )

    result["Overstock_Risk"] = np.where(
        result["Excess_Stock"] > 0,
        "HIGH",
        "LOW"
    )

    # -----------------------------------------------------
    # OVERALL RISK
    # -----------------------------------------------------

    result["Overall_Risk"] = "LOW"

    result.loc[
        result["Stockout_Risk"] == "HIGH",
        "Overall_Risk"
    ] = "HIGH"

    result.loc[
        (
            (result["Stockout_Risk"] == "HIGH") |
            (result["Overstock_Risk"] == "HIGH")
        ),
        "Overall_Risk"
    ] = "HIGH"

    # -----------------------------------------------------
    # BUSINESS DECISION
    # -----------------------------------------------------

    result["Recommendation"] = "HEALTHY"

    result.loc[
        result["Stockout_Risk"] == "HIGH",
        "Recommendation"
    ] = "REORDER NOW"

    result.loc[
        (
            (result["Stockout_Risk"] == "LOW") &
            (result["Overstock_Risk"] == "HIGH")
        ),
        "Recommendation"
    ] = "MARKDOWN / CLEAR"

    # Existing reorder point information
    # is also considered.

    result.loc[
        (
            (result["Current_Stock"] <= result["Reorder_Point"]) &
            (result["Stockout_Risk"] == "LOW")
        ),
        "Recommendation"
    ] = "REORDER SOON"

    # -----------------------------------------------------
    # RISK SCORE
    # -----------------------------------------------------

    result["Risk_Score"] = 0

    result.loc[
        result["Stockout_Risk"] == "HIGH",
        "Risk_Score"
    ] += 60

    result.loc[
        result["Overstock_Risk"] == "HIGH",
        "Risk_Score"
    ] += 40

    # Cap score at 100
    result["Risk_Score"] = (
        result["Risk_Score"].clip(upper=100)
    )

    return result


# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------

def generate_risk_summary(risk_df):

    summary = {
        "total_skus": len(risk_df),

        "high_risk": int(
            (risk_df["Overall_Risk"] == "HIGH").sum()
        ),

        "stockout_risk": int(
            (risk_df["Stockout_Risk"] == "HIGH").sum()
        ),

        "overstock_risk": int(
            (risk_df["Overstock_Risk"] == "HIGH").sum()
        ),

        "reorder_now": int(
            (
                risk_df["Recommendation"] ==
                "REORDER NOW"
            ).sum()
        ),

        "reorder_soon": int(
            (
                risk_df["Recommendation"] ==
                "REORDER SOON"
            ).sum()
        ),

        "markdown_clear": int(
            (
                risk_df["Recommendation"] ==
                "MARKDOWN / CLEAR"
            ).sum()
        ),

        "healthy": int(
            (
                risk_df["Recommendation"] ==
                "HEALTHY"
            ).sum()
        )
    }

    return summary