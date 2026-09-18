import pandas as pd
from lightgbm import LGBMRegressor

FEATURES = [
    'Price',
    'Promotion',
    'lag_1',
    'lag_2',
    'lag_4',
    'lag_52',
    'rolling_mean_4',
    'rolling_mean_8',
    'rolling_mean_12',
    'Week_Num',
    'Month'
]


def train_lgbm(train_df: pd.DataFrame) -> LGBMRegressor:
    """Trains a LightGBM Regressor on feature matrix."""
    
    X_train = train_df[FEATURES]
    y_train = train_df['Units_Sold']

    model = LGBMRegressor(
        n_estimators=150,
        learning_rate=0.05,
        max_depth=5,
        random_state=42,
        verbosity=-1
    )

    model.fit(X_train, y_train)

    return model


def generate_future_forecast(
    model: LGBMRegressor,
    historical_df: pd.DataFrame,
    weeks_ahead: int = 12
) -> pd.DataFrame:
    """
    Generates recursive future demand forecasts for every SKU.

    Previous predictions are used as demand history for later future weeks.
    """

    df = historical_df.copy()

    df['Week_Start'] = pd.to_datetime(df['Week_Start'])
    df = df.sort_values(['SKU', 'Week_Start'])

    results = []

    for sku in df['SKU'].unique():

        sku_df = df[df['SKU'] == sku].copy()
        sku_df = sku_df.sort_values('Week_Start').reset_index(drop=True)

        history = sku_df['Units_Sold'].tolist()

        last_date = sku_df['Week_Start'].max()

        last_price = sku_df['Price'].iloc[-1]
        last_promotion = sku_df['Promotion'].iloc[-1]

        for step in range(1, weeks_ahead + 1):

            future_date = last_date + pd.Timedelta(weeks=step)

            lag_1 = history[-1]
            lag_2 = history[-2]
            lag_4 = history[-4]

            if len(history) >= 52:
                lag_52 = history[-52]
            else:
                lag_52 = history[0]

            rolling_mean_4 = sum(history[-4:]) / min(4, len(history))
            rolling_mean_8 = sum(history[-8:]) / min(8, len(history))
            rolling_mean_12 = sum(history[-12:]) / min(12, len(history))

            week_num = int(future_date.isocalendar().week)
            month = future_date.month

            future_features = pd.DataFrame([{
                'Price': last_price,
                'Promotion': last_promotion,
                'lag_1': lag_1,
                'lag_2': lag_2,
                'lag_4': lag_4,
                'lag_52': lag_52,
                'rolling_mean_4': rolling_mean_4,
                'rolling_mean_8': rolling_mean_8,
                'rolling_mean_12': rolling_mean_12,
                'Week_Num': week_num,
                'Month': month
            }])

            prediction = float(model.predict(future_features)[0])

            # Demand cannot be negative.
            prediction = max(0.0, prediction)

            results.append({
                'SKU': sku,
                'Week_Start': future_date,
                'Forecast_Units': prediction
            })

            # Use prediction as history for next future week.
            history.append(prediction)

    return pd.DataFrame(results)
