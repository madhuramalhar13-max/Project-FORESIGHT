import pandas as pd
from lightgbm import LGBMRegressor

FEATURES = [
    'Price', 'Promotion', 'lag_1', 'lag_2', 'lag_4', 'lag_52',
    'rolling_mean_4', 'rolling_mean_8', 'rolling_mean_12',
    'Week_Num', 'Month'
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
