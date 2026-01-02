import numpy as np
from model import V_MIN, V_MAX

def stress_profile(P, factor=1.1):
    """Increases load/generation by a factor (e.g., 10%) to test fragility."""
    return P * factor

def calculate_safety_margin(V):
    """
    Calculates the minimum distance from statutory limits.
    A higher margin indicates a more 'robust' network.
    """
    if V is None: return -1.0
    margin_low = np.min(V - V_MIN)
    margin_high = np.min(V_MAX - V)
    return min(margin_low, margin_high)