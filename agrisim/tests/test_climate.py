import numpy as np
from agrisim.config.simulation_config import SimulationConfig
from agrisim.climate.markov_engine import MarkovClimateEngine

def test_climate_reproducibility():
    config = SimulationConfig(random_seed=42)
    engine1 = MarkovClimateEngine(config)
    states1, rain1, temp1 = engine1.generate_sequence(10)
    
    config = SimulationConfig(random_seed=42)
    engine2 = MarkovClimateEngine(config)
    states2, rain2, temp2 = engine2.generate_sequence(10)
    
    np.testing.assert_array_equal(states1, states2)
    np.testing.assert_array_equal(rain1, rain2)
    np.testing.assert_array_equal(temp1, temp2)

def test_state_transitions():
    config = SimulationConfig()
    engine = MarkovClimateEngine(config)
    # Just run it to ensure no exceptions and values are valid
    states, rain, temp = engine.generate_sequence(100)
    assert len(states) == 100
    assert all(s in [0, 1, 2] for s in states)
    assert all(r >= 0 for r in rain)
