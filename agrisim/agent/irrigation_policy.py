from abc import ABC, abstractmethod
from agrisim.config.simulation_config import SimulationConfig
from agrisim.climate.climate_states import ClimateState

class BasePolicy(ABC):
    """Abstract base class for farmer decision policies."""
    
    def __init__(self, config: SimulationConfig):
        self.config = config
        self.total_water_used = 0.0
        
    @abstractmethod
    def decide_irrigation(self, current_soil_moisture: float, current_climate_state: ClimateState) -> float:
        pass

class NoIrrigationPolicy(BasePolicy):
    """Baseline policy: no irrigation is ever applied."""
    
    def decide_irrigation(self, current_soil_moisture: float, current_climate_state: ClimateState) -> float:
        return 0.0

class ThresholdPolicy(BasePolicy):
    """Deterministic policy irrigating fixed amounts when below a threshold."""
    
    def decide_irrigation(self, current_soil_moisture: float, current_climate_state: ClimateState) -> float:
        if current_soil_moisture < self.config.irrigation_threshold:
            irrigation_amount = self.config.irrigation_amount
            self.total_water_used += irrigation_amount
            return irrigation_amount
        return 0.0

class AdaptivePolicy(BasePolicy):
    """Adaptive policy that lowers the threshold during known drought conditions to conserve water."""
    
    def decide_irrigation(self, current_soil_moisture: float, current_climate_state: ClimateState) -> float:
        # If in severe drought, farmer accepts higher stress to save water (threshold drops)
        effective_threshold = self.config.irrigation_threshold
        if current_climate_state == ClimateState.DROUGHT_EXTREME:
            effective_threshold *= 0.5
        elif current_climate_state == ClimateState.PRE_DROUGHT:
            effective_threshold *= 0.8
            
        if current_soil_moisture < effective_threshold:
            irrigation_amount = self.config.irrigation_amount
            self.total_water_used += irrigation_amount
            return irrigation_amount
        return 0.0
