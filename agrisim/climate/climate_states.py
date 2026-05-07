from enum import IntEnum

class ClimateState(IntEnum):
    """Hidden states for the climate Markov engine."""
    NORMAL = 0
    PRE_DROUGHT = 1
    DROUGHT_EXTREME = 2
