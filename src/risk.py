import pandas as pd
import numpy as np


def calculate_inventory_risk(forecast_df, inventory_df):

    forecast_df = forecast_df.copy()
    inventory_df = inventory_df.copy()

    forecast_df.columns = forecast_df.columns.str.strip()
    inventory_df.columns = inventory_df.columns.str.strip()

    # Calculate average forecast demand for each SKU
    average_forecast = (
        forecast_df
        .groupby("SKU")["Forecast_Units"]
        .mean()
        .reset_index()
    )

    average_forecast.rename(
        columns={
            "Forecast_Units": "Average_Forecast_Demand"
        },
        inplace=True
    )

    # Merge forecast with inventory
    risk_df = inventory_df.merge(
        average_forecast,
        on="SKU",
        how="left"
    )

    # Handle missing forecast values
    risk_df["Average_Forecast_Demand"] = (
        risk_df["Average_Forecast_Demand"]
        .fillna(0)
    )

    risk_df["Average_Forecast_Demand"] = (
        risk_df["Average_Forecast_Demand"]
        .replace(0, np.nan)
    )

    # Calculate stock coverage
    risk_df["Stock_Coverage_Weeks"] = (
        risk_df["Current_Stock"] /
        risk_df["Average_Forecast_Demand"]
    )

    risk_df["Stock_Coverage_Weeks"] = (
        risk_df["Stock_Coverage_Weeks"]
        .replace([np.inf, -np.inf], np.nan)
        .fillna(0)
    )

    # Convert lead time from days to weeks
    risk_df["Lead_Time_Weeks"] = (
        risk_df["Lead_Time_Days"] / 7
    )

    # Demand expected during lead time
    risk_df["Lead_Time_Demand"] = (
        risk_df["Average_Forecast_Demand"] *
        risk_df["Lead_Time_Weeks"]
    )

    # Current stock + stock already ordered
    risk_df["Available_Stock"] = (
        risk_df["Current_Stock"] +
        risk_df["On_Order"]
    )

    # Calculate stockout gap
    risk_df["Stockout_Gap"] = (
        risk_df["Lead_Time_Demand"] +
        risk_df["Safety_Stock"] -
        risk_df["Available_Stock"]
    )

    # Stockout risk
    risk_df["Stockout_Risk"] = np.where(
        risk_df["Stockout_Gap"] > 0,
        "HIGH",
        "LOW"
    )

    # Overstock calculation
    target_inventory = (
        risk_df["Average_Forecast_Demand"] * 12
    )

    risk_df["Excess_Stock"] = (
        risk_df["Current_Stock"] -
        target_inventory
    )

    risk_df["Overstock_Risk"] = np.where(
        risk_df["Excess_Stock"] > 0,
        "HIGH",
        "LOW"
    )

    # Overall risk
    risk_df["Overall_Risk"] = np.where(
        (risk_df["Stockout_Risk"] == "HIGH") |
        (risk_df["Overstock_Risk"] == "HIGH"),
        "HIGH",
        "LOW"
    )

    # Recommendations
    risk_df["Recommendation"] = "HEALTHY"

    risk_df.loc[
        risk_df["Stockout_Risk"] == "HIGH",
        "Recommendation"
    ] = "REORDER NOW"

    risk_df.loc[
        (risk_df["Stockout_Risk"] == "LOW") &
        (risk_df["Overstock_Risk"] == "HIGH"),
        "Recommendation"
    ] = "MARKDOWN / CLEAR"

    risk_df.loc[
        (risk_df["Stockout_Risk"] == "LOW") &
        (risk_df["Overstock_Risk"] == "LOW") &
        (risk_df["Current_Stock"] <= risk_df["Reorder_Point"]),
        "Recommendation"
    ] = "REORDER SOON"

    # Risk score
    risk_df["Risk_Score"] = 0

    risk_df.loc[
        risk_df["Stockout_Risk"] == "HIGH",
        "Risk_Score"
    ] += 60

    risk_df.loc[
        risk_df["Overstock_Risk"] == "HIGH",
        "Risk_Score"
    ] += 40

    risk_df["Risk_Score"] = (
        risk_df["Risk_Score"].clip(0, 100)
    )

    return risk_df


def generate_risk_summary(risk_df):

    return {
        "total_skus": len(risk_df),

        "high_risk": len(
            risk_df[
                risk_df["Overall_Risk"] == "HIGH"
            ]
        ),

        "stockout_risk": len(
            risk_df[
                risk_df["Stockout_Risk"] == "HIGH"
            ]
        ),

        "overstock_risk": len(
            risk_df[
                risk_df["Overstock_Risk"] == "HIGH"
            ]
        ),

        "reorder_now": len(
            risk_df[
                risk_df["Recommendation"] == "REORDER NOW"
            ]
        ),

        "reorder_soon": len(
            risk_df[
                risk_df["Recommendation"] == "REORDER SOON"
            ]
        ),

        "markdown_clear": len(
            risk_df[
                risk_df["Recommendation"] == "MARKDOWN / CLEAR"
            ]
        ),

        "healthy": len(
            risk_df[
                risk_df["Recommendation"] == "HEALTHY"
            ]
        )
    }