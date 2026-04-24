import math

def calc_max_error(error_array):
    return max(error_array)

def calc_mae(error_array):
    return sum(error_array) / len(error_array)

def calc_rmse(error_array):
    n = len(error_array)
    return math.sqrt(sum(e**2 for e in error_array) / n)

def calc_mape(error_array, exact_array):
    n = len(error_array)
    eps = 1e-16 # Prevents division by zero just in case
    
    # Formula: (Error / Exact_Value) 
    total_pct_error = sum(e / (abs(exact_val) + eps) for e, exact_val in zip(error_array, exact_array))
    
    return (total_pct_error / n) * 100.0