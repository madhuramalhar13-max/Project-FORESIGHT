import pandas as pd
import numpy as np

def prepare_weekly_demand(df_sales: pd.DataFrame, df_calendar: pd.DataFrame) -> pd.DataFrame:
    """Aggregates daily sales to weekly SKU-level demand and merges calendar attributes."""
    sales = df_sales.copy()
    sales['Date'] = pd.to_datetime(sales['Date'])
    
    weekly_sales = (
        sales.groupby(['SKU', pd.Grouper(key='Date', freq='W-MON')])
        .agg(
            Units_Sold=('Units_Sold', 'sum'),
            Price=('Price', 'mean'),
            Promotion=('Promotion', 'max')
        )
        .reset_index()
        .rename(columns={'Date': 'Week_Start'})
    )
    
    cal = df_calendar.copy()
    cal['date'] = pd.to_datetime(cal['date'])
    weekly_cal = (
        cal.groupby(pd.Grouper(key='date', freq='W-MON'))
        .agg(
            Is_Holiday=('is_holiday', 'max'),
            Promotion_Event=('promotion_event', lambda x: 1 if x.dropna().count() > 0 else 0)
        )
        .reset_index()
        .rename(columns={'date': 'Week_Start'})
    )
    
    weekly_df = pd.merge(weekly_sales, weekly_cal, on='Week_Start', how='left').sort_values(['SKU', 'Week_Start'])
    return weekly_df

def build_lag_and_rolling_features(df_weekly: pd.DataFrame) -> pd.DataFrame:
    """Generates seasonal lag (52-week), historical lags, rolling statistics, and temporal features."""
    df = df_weekly.copy().sort_values(['SKU', 'Week_Start'])
    
    for lag in [1, 2, 4, 52]:
        df[f'lag_{lag}'] = df.groupby('SKU')['Units_Sold'].shift(lag)
        
    for window in [4, 8, 12]:
        df[f'rolling_mean_{window}'] = (
            df.groupby('SKU')['Units_Sold']
            .transform(lambda x: x.shift(1).rolling(window=window).mean())
        )
        
    df['Week_Num'] = df['Week_Start'].dt.isocalendar().week.astype(int)
    df['Month'] = df['Week_Start'].dt.month
    df['Year'] = df['Week_Start'].dt.year
    
    return df
