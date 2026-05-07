from agrisim.config.simulation_config import SimulationConfig

class CropModel:
    """Basic crop biomass accumulation model."""
    
    def __init__(self, config: SimulationConfig):
        self.config = config
        self.current_biomass = config.initial_biomass
        
    def step(self, soil_moisture: float, temperature: float) -> float:
        """
        Updates the crop biomass based on environmental conditions.
        
        Args:
            soil_moisture (float): Current soil moisture in mm.
            temperature (float): Current temperature in C.
            
        Returns:
            float: Updated crop biomass (kg/ha).
        """
        # Moisture stress factor (0 to 1)
        # Optimal moisture is assumed to be > 50% of max
        optimal_moisture = self.config.max_soil_moisture * 0.5
        if soil_moisture >= optimal_moisture:
            water_stress_factor = 1.0
        else:
            water_stress_factor = max(0.0, soil_moisture / optimal_moisture)
            
        # Temperature stress factor
        # Assume optimal temperature is around 25C
        if 20.0 <= temperature <= 30.0:
            temp_stress_factor = 1.0
        else:
            temp_stress_factor = max(0.1, 1.0 - abs(temperature - 25.0) / 15.0)
            
        # Logistic growth limited by carrying capacity (max_biomass)
        growth_potential = self.config.base_growth_rate * self.current_biomass * (1.0 - self.current_biomass / self.config.max_biomass)
        
        actual_growth = growth_potential * water_stress_factor * temp_stress_factor
        
        self.current_biomass += actual_growth
        
        return self.current_biomass
