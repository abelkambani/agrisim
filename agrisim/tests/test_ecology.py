from agrisim.config.simulation_config import SimulationConfig
from agrisim.ecology.lotka_volterra import LotkaVolterraEcology

def test_ecology_bounds():
    config = SimulationConfig()
    ecology = LotkaVolterraEcology(config)
    
    # Run a step with optimal conditions
    biomass, pests = ecology.step(soil_moisture=100.0, temperature=25.0)
    
    assert biomass > 0.0
    assert pests >= 0.0
    
def test_pest_growth():
    config = SimulationConfig()
    # High conversion rate to force pest growth
    config.pest_conversion_rate = 0.05
    ecology = LotkaVolterraEcology(config)
    
    initial_pests = ecology.current_pests
    _, new_pests = ecology.step(soil_moisture=100.0, temperature=25.0)
    
    # Pests should grow if there is crop
    assert new_pests > initial_pests
