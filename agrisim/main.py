import sys
import os
import pandas as pd
from agrisim.config.simulation_config import SimulationConfig
from agrisim.agent.irrigation_policy import ThresholdPolicy
from agrisim.analytics.experiment_runner import run_monte_carlo
from agrisim.analytics.statistical_summaries import summarize_monte_carlo, generate_comparative_summary

def main():
    """CLI entrypoint for running headless experiments."""
    print("Initializing Agrisim Computational Study...")
    
    config = SimulationConfig()
    
    print("Running Baseline Experiment (Threshold Policy)...")
    runs = run_monte_carlo(config, ThresholdPolicy, n_simulations=5)
    
    print(f"Completed {len(runs)} Monte Carlo trajectories.")
    
    summary_df = summarize_monte_carlo(runs)
    print("\nSummary Results:")
    print(summary_df)
    
    # Save a quick CSV
    output_path = os.path.join(os.path.dirname(__file__), 'baseline_experiment.csv')
    pd.concat(runs).to_csv(output_path, index=False)
    print(f"\nRaw trajectory data saved to {output_path}")
    
    print("\nTo launch the interactive dashboard, run:")
    print("streamlit run agrisim/dashboard/app.py")

if __name__ == "__main__":
    main()
