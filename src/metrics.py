import numpy as np

def calculate_wape(y_true, y_pred) -> float:
    """
    Calculates Weighted Absolute Percentage Error (WAPE).
    WAPE = sum(|y_true - y_pred|) / sum(|y_true|)
    """
    y_true = np.array(y_true, dtype=float)
    y_pred = np.array(y_pred, dtype=float)
    
    total_actual = np.sum(np.abs(y_true))
    if total_actual == 0:
        return 0.0
    return float(np.sum(np.abs(y_true - y_pred)) / total_actual)
