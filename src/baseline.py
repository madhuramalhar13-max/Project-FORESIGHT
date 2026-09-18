import pandas as pd

class SeasonalNaiveBaseline:
    """Seasonal Naive model predicting demand using 52-week lag with lag_1 fallback."""
    def __init__(self, seasonality: int = 52):
        self.seasonality = seasonality

    def predict(self, df: pd.DataFrame) -> pd.Series:
        if f'lag_{self.seasonality}' in df.columns:
            preds = df[f'lag_{self.seasonality}']
        else:
            preds = df.groupby('SKU')['Units_Sold'].shift(self.seasonality)
            
        fallback = df['lag_1'] if 'lag_1' in df.columns else df.groupby('SKU')['Units_Sold'].shift(1)
        return preds.fillna(fallback).fillna(0)
