from agrisim.config.simulation_config import SimulationConfig

def get_scenario_config(scenario_name: str) -> SimulationConfig:
    """Returns a pre-configured SimulationConfig based on the scenario preset."""
    config = SimulationConfig()
    
    if scenario_name == "🌵 Drought Scenario":
        # Force high probability of moving to and staying in DROUGHT_EXTREME
        config.transition_matrix[0] = [0.2, 0.5, 0.3]
        config.transition_matrix[1] = [0.1, 0.3, 0.6]
        config.transition_matrix[2] = [0.05, 0.15, 0.8]
        config.initial_soil_moisture = 40.0
        
    elif scenario_name == "🌧️ Normal Climate":
        # High probability of NORMAL
        config.transition_matrix[0] = [0.90, 0.08, 0.02]
        config.transition_matrix[1] = [0.40, 0.50, 0.10]
        config.transition_matrix[2] = [0.20, 0.40, 0.40]
        config.initial_soil_moisture = 80.0
        
    elif scenario_name == "🌾 Optimized Farming":
        # Normal climate, but very resilient crop parameters
        config.crop_growth_rate = 0.15
        config.max_biomass = 12000.0
        config.pest_conversion_rate = 0.0005 # Less susceptible to pests
        
    elif scenario_name == "🔥 Extreme Heat Stress":
        # Normal rainfall probs, but temperatures are extremely high, causing massive ET
        config.temp_params = {
            0: (30.0, 3.0),
            1: (35.0, 4.0),
            2: (40.0, 5.0)
        }
        config.evapotranspiration_base = 6.0
        
    return config
