import pandas as pd
import numpy as np
from typing import List

def compute_cvar(returns: np.ndarray, alpha: float = 0.05) -> float:
    """Computes the Conditional Value at Risk (Expected Shortfall) at the given alpha level.
    Assuming 'returns' are yields or positive metrics where lower is worse.
    """
    if len(returns) == 0:
        return 0.0
    var_threshold = np.percentile(returns, alpha * 100)
    tail_values = returns[returns <= var_threshold]
    if len(tail_values) == 0:
        return var_threshold
    return np.mean(tail_values)

def summarize_monte_carlo(runs: List[pd.DataFrame]) -> pd.DataFrame:
    """Summarizes a list of Monte Carlo runs into key metrics per run."""
    summaries = []
    
    for df in runs:
        run_id = df['run_id'].iloc[0]
        # Final yield is the crop biomass at the last timestep
        final_yield = df['crop_biomass'].iloc[-1]
        total_irrigation = df['irrigation'].sum()
        max_pests = df['pest_population'].max()
        drought_days = (df['state'] == 'DROUGHT_EXTREME').sum()
        
        summaries.append({
            'run_id': run_id,
            'final_yield': final_yield,
            'total_irrigation': total_irrigation,
            'max_pests': max_pests,
            'drought_days': drought_days
        })
        
    return pd.DataFrame(summaries)

def generate_comparative_summary(policy_summaries: dict) -> pd.DataFrame:
    """
    Takes a dictionary mapping policy_name -> summaries_df
    and computes aggregate statistics (Mean Yield, CVaR Yield, Mean Water).
    """
    records = []
    for policy_name, df in policy_summaries.items():
        yields = df['final_yield'].values
        mean_yield = np.mean(yields)
        cvar_yield = compute_cvar(yields, alpha=0.10) # 10% worst cases
        mean_water = df['total_irrigation'].mean()
        mean_pests = df['max_pests'].mean()
        
        records.append({
            'Policy': policy_name,
            'Mean Yield (kg/ha)': mean_yield,
            'CVaR Yield 10% (kg/ha)': cvar_yield,
            'Mean Water Used (mm)': mean_water,
            'Mean Max Pests': mean_pests
        })
        
    return pd.DataFrame(records)
