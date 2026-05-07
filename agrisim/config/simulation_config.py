import numpy as np
from dataclasses import dataclass, field
from typing import Dict, Tuple

@dataclass
class SimulationConfig:
    """Master configuration for the Agrisim simulation."""
    
    # Global Random Seed for Reproducibility
    random_seed: int = 42
    
    # Simulation Parameters
    total_timesteps: int = 180  # e.g., days in a growing season
    
    # Climate Markov Engine Parameters
    # State space: 0: NORMAL, 1: PRE_DROUGHT, 2: DROUGHT_EXTREME
    transition_matrix: np.ndarray = field(default_factory=lambda: np.array([
        [0.85, 0.10, 0.05], # From NORMAL
        [0.20, 0.60, 0.20], # From PRE_DROUGHT
        [0.10, 0.30, 0.60]  # From DROUGHT_EXTREME
    ]))
    
    # Rainfall distributions (Gamma distribution parameters: shape, scale) per state
    # Shape, Scale. Mean = shape * scale.
    rainfall_params: Dict[int, Tuple[float, float]] = field(default_factory=lambda: {
        0: (2.0, 5.0),   # NORMAL: Mean 10mm
        1: (1.5, 2.0),   # PRE_DROUGHT: Mean 3mm
        2: (0.5, 1.0)    # DROUGHT_EXTREME: Mean 0.5mm
    })
    
    # Temperature distributions (Normal distribution parameters: mean, std) per state
    temp_params: Dict[int, Tuple[float, float]] = field(default_factory=lambda: {
        0: (25.0, 3.0),  # NORMAL: 25C mean
        1: (28.0, 4.0),  # PRE_DROUGHT: 28C mean
        2: (32.0, 5.0)   # DROUGHT_EXTREME: 32C mean
    })
    
    # Soil Parameters
    max_soil_moisture: float = 100.0 # mm
    initial_soil_moisture: float = 80.0 # mm
    evapotranspiration_base: float = 4.0 # mm/day under normal conditions
    
    # Ecology (Lotka-Volterra) Parameters
    max_biomass: float = 10000.0 # kg/ha
    initial_biomass: float = 100.0 # kg/ha
    crop_growth_rate: float = 0.1 # intrinsic growth rate (alpha)
    
    initial_pest_population: float = 5.0 # arbitrary units
    predation_rate: float = 0.002 # rate at which pests consume crop (beta)
    pest_conversion_rate: float = 0.001 # conversion of crop biomass to pest population (delta)
    pest_death_rate: float = 0.1 # natural death rate of pests (gamma)
    pest_carrying_capacity: float = 500.0 # max pests
    
    # Irrigation Parameters
    irrigation_amount: float = 20.0 # mm per irrigation event
    irrigation_threshold: float = 40.0 # mm trigger point
