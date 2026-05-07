import numpy as np
import pandas as pd
from typing import List, Type
from agrisim.config.simulation_config import SimulationConfig
from agrisim.climate.markov_engine import MarkovClimateEngine
from agrisim.soil.moisture_balance import SoilMoistureModel
from agrisim.ecology.lotka_volterra import LotkaVolterraEcology
from agrisim.agent.irrigation_policy import BasePolicy

def run_single_simulation(config: SimulationConfig, policy_class: Type[BasePolicy]) -> pd.DataFrame:
    """Runs a single simulation and returns a DataFrame of the results."""
    climate = MarkovClimateEngine(config)
    soil = SoilMoistureModel(config)
    ecology = LotkaVolterraEcology(config)
    agent = policy_class(config)
    
    results = []
    
    for t in range(config.total_timesteps):
        state, rainfall, temperature = climate.step()
        
        irrigation = agent.decide_irrigation(soil.current_moisture, state)
        
        current_moisture = soil.step(rainfall, temperature, ecology.current_biomass, irrigation)
        
        current_biomass, current_pests = ecology.step(current_moisture, temperature)
        
        results.append({
            'timestep': t,
            'state': state.name,
            'rainfall': rainfall,
            'temperature': temperature,
            'soil_moisture': current_moisture,
            'irrigation': irrigation,
            'crop_biomass': current_biomass,
            'pest_population': current_pests
        })
        
    return pd.DataFrame(results)

def run_monte_carlo(base_config: SimulationConfig, policy_class: Type[BasePolicy], n_simulations: int = 10) -> List[pd.DataFrame]:
    """Runs N simulations with different random seeds."""
    all_runs = []
    for i in range(n_simulations):
        # Create a new config with a different seed
        run_config = SimulationConfig(
            random_seed=base_config.random_seed + i,
            irrigation_threshold=base_config.irrigation_threshold,
            irrigation_amount=base_config.irrigation_amount
        )
        df = run_single_simulation(run_config, policy_class)
        df['run_id'] = i
        all_runs.append(df)
        
    return all_runs
