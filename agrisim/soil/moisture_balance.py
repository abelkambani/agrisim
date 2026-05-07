from agrisim.config.simulation_config import SimulationConfig

class SoilMoistureModel:
    """Dynamic soil moisture tracking model."""
    
    def __init__(self, config: SimulationConfig):
        self.config = config
        self.current_moisture = config.initial_soil_moisture
        self.max_moisture = config.max_soil_moisture
        
    def step(self, rainfall: float, temperature: float, crop_biomass: float, irrigation: float) -> float:
        """
        Updates the soil moisture state based on water inputs and outputs.
        
        Args:
            rainfall (float): Daily rainfall input in mm.
            temperature (float): Daily mean temperature in C.
            crop_biomass (float): Current crop biomass (influences transpiration).
            irrigation (float): Applied irrigation water in mm.
            
        Returns:
            float: The updated soil moisture level (mm).
        """
        # Inputs
        total_input = rainfall + irrigation
        
        # Outputs (Evapotranspiration)
        # Simplified ET calculation: base ET modulated by temperature anomaly and crop presence
        temp_factor = max(0.5, temperature / 25.0) # Assume 25C is baseline
        crop_factor = 1.0 + (crop_biomass / self.config.max_biomass) * 0.5 # Crop increases ET
        
        et_demand = self.config.evapotranspiration_base * temp_factor * crop_factor
        
        # Actual ET is limited by available moisture
        actual_et = min(et_demand, self.current_moisture + total_input)
        
        # Update state
        new_moisture = self.current_moisture + total_input - actual_et
        
        # Cap at max capacity (excess lost to deep percolation/runoff)
        self.current_moisture = min(self.max_moisture, max(0.0, new_moisture))
        
        return self.current_moisture
