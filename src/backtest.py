import pandas as pd
from src.baseline import SeasonalNaiveBaseline
from src.forecast import train_lgbm, FEATURES
from src.metrics import calculate_wape

def run_rolling_backtest(df_weekly: pd.DataFrame, n_splits: int = 4, forecast_horizon: int = 4):
    """Executes rolling-origin backtest comparing LightGBM vs Seasonal-Naive baseline via WAPE."""
    unique_weeks = sorted(df_weekly['Week_Start'].unique())
    results = []

    for i in range(n_splits):
        cutoff_idx = len(unique_weeks) - (n_splits - i) * forecast_horizon
        cutoff_date = unique_weeks[cutoff_idx]
        
        train = df_weekly[df_weekly['Week_Start'] <= cutoff_date].dropna(subset=FEATURES)
        test = df_weekly[
            (df_weekly['Week_Start'] > cutoff_date) & 
            (df_weekly['Week_Start'] <= unique_weeks[min(cutoff_idx + forecast_horizon, len(unique_weeks) - 1)])
        ].copy()
        
        if test.empty:
            continue
            
        baseline_model = SeasonalNaiveBaseline(seasonality=52)
        test['pred_baseline'] = baseline_model.predict(test)
        
        lgbm = train_lgbm(train)
        test['pred_lgbm'] = lgbm.predict(test[FEATURES])
        
        wape_base = calculate_wape(test['Units_Sold'], test['pred_baseline'])
        wape_lgbm = calculate_wape(test['Units_Sold'], test['pred_lgbm'])
        
        results.append({
            'Fold': i + 1,
            'Cutoff_Date': cutoff_date.strftime('%Y-%m-%d'),
            'WAPE_Baseline': round(wape_base, 4),
            'WAPE_LGBM': round(wape_lgbm, 4)
        })
        
    return pd.DataFrame(results)
