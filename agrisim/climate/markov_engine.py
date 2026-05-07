import numpy as np
from typing import Tuple
from agrisim.config.simulation_config import SimulationConfig
from agrisim.climate.climate_states import ClimateState

class MarkovClimateEngine:
    """
    Discrete-time Markov chain climate engine generating stochastic weather variables
    conditioned on hidden climate states.
    """
    def __init__(self, config: SimulationConfig):
        self.config = config
        self.rng = np.random.default_rng(config.random_seed)
        self.current_state = ClimateState.NORMAL
        
    def step(self) -> Tuple[ClimateState, float, float]:
        """
        Advances the climate engine by one timestep.
        
        Returns:
            Tuple containing:
            - next_state (ClimateState): The new climate state.
            - rainfall (float): Sampled rainfall (mm).
            - temperature (float): Sampled temperature (C).
        """
        # 1. State Transition
        transition_probs = self.config.transition_matrix[self.current_state.value]
        next_state_value = self.rng.choice(
            [state.value for state in ClimateState],
            p=transition_probs
        )
        self.current_state = ClimateState(next_state_value)
        
        # 2. Sample Weather Variables Conditioned on State
        rain_shape, rain_scale = self.config.rainfall_params[self.current_state.value]
        # Gamma distribution for rainfall; handle edge case where scale/shape might be very small
        rainfall = self.rng.gamma(shape=rain_shape, scale=rain_scale)
        
        temp_mean, temp_std = self.config.temp_params[self.current_state.value]
        temperature = self.rng.normal(loc=temp_mean, scale=temp_std)
        
        return self.current_state, max(0.0, rainfall), temperature
        
    def generate_sequence(self, timesteps: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Generates a full sequence of climate variables."""
        states = np.zeros(timesteps, dtype=int)
        rainfall = np.zeros(timesteps)
        temperature = np.zeros(timesteps)
        
        for t in range(timesteps):
            state, rain, temp = self.step()
            states[t] = state.value
            rainfall[t] = rain
            temperature[t] = temp
            
        return states, rainfall, temperature
