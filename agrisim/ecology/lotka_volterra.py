import numpy as np
from scipy.integrate import solve_ivp
from typing import Tuple
from agrisim.config.simulation_config import SimulationConfig

class LotkaVolterraEcology:
    """
    Continuous Lotka-Volterra model for Crop-Pest dynamics, solved over a daily timestep.
    """
    def __init__(self, config: SimulationConfig):
        self.config = config
        self.current_biomass = config.initial_biomass
        self.current_pests = config.initial_pest_population
        
    def step(self, soil_moisture: float, temperature: float) -> Tuple[float, float]:
        """
        Advances the ecological state by one day (t=0 to t=1).
        
        Args:
            soil_moisture (float): Current soil moisture in mm.
            temperature (float): Current temperature in C.
            
        Returns:
            Tuple[float, float]: Updated crop biomass and pest population.
        """
        # Modulate crop growth rate by environmental stress
        optimal_moisture = self.config.max_soil_moisture * 0.5
        water_stress_factor = 1.0 if soil_moisture >= optimal_moisture else max(0.0, soil_moisture / optimal_moisture)
        
        temp_stress_factor = 1.0 if 20.0 <= temperature <= 30.0 else max(0.1, 1.0 - abs(temperature - 25.0) / 15.0)
        
        effective_crop_growth = self.config.crop_growth_rate * water_stress_factor * temp_stress_factor
        
        def dynamics(t, y):
            crop, pest = y
            # Protect against numerical issues
            crop = max(0.0, crop)
            pest = max(0.0, pest)
            
            # Logistic growth for crop, minus predation
            # dC/dt = r*C*(1 - C/K) - beta*C*P
            dc_dt = effective_crop_growth * crop * (1.0 - crop / self.config.max_biomass) - self.config.predation_rate * crop * pest
            
            # Pest growth: conversion of crop to pests minus death rate, limited by carrying capacity
            # dP/dt = delta*C*P - gamma*P
            dp_dt = self.config.pest_conversion_rate * crop * pest - self.config.pest_death_rate * pest
            dp_dt = dp_dt * (1.0 - pest / self.config.pest_carrying_capacity)
            
            return [dc_dt, dp_dt]
            
        # Solve IVP for 1 day
        sol = solve_ivp(dynamics, [0, 1], [self.current_biomass, self.current_pests], method='RK45')
        
        self.current_biomass = max(0.0, sol.y[0][-1])
        self.current_pests = max(0.0, sol.y[1][-1])
        
        return self.current_biomass, self.current_pests
