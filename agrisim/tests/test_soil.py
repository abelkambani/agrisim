from agrisim.config.simulation_config import SimulationConfig
from agrisim.soil.moisture_balance import SoilMoistureModel

def test_soil_mass_balance():
    config = SimulationConfig()
    soil = SoilMoistureModel(config)
    
    initial = soil.current_moisture
    # Add rain, high temp to cause ET, no irrigation, no crop
    new_moisture = soil.step(rainfall=10.0, temperature=25.0, crop_biomass=0.0, irrigation=0.0)
    
    assert new_moisture > 0
    assert new_moisture <= config.max_soil_moisture
    # Rough check: initial(80) + rain(10) - ET(4) = 86
    assert abs(new_moisture - 86.0) < 0.1
    
    # Test capping
    new_moisture_capped = soil.step(rainfall=100.0, temperature=25.0, crop_biomass=0.0, irrigation=0.0)
    assert new_moisture_capped == config.max_soil_moisture
