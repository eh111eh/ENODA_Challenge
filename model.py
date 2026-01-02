import numpy as np

# Statutory limits and nominal values
V_MIN = 207.0
V_MAX = 253.0
V_NOMINAL = 230.0

def compute_voltages(V0, P_injections, R_seg):
    """
    Sequential quadratic voltage model.
    P_injections: List of power values from node 1 to N-1 (p0 excluded).
    R_seg: Resistance of a single line segment (L * R).
    Returns an array of voltages [V0, V1, ..., VN-1] or None if infeasible.
    """
    V = [V0]
    for pk in P_injections:
        Vk = V[-1]
        # Governing equation: Vk+1^2 - Vk*Vk+1 - PR = 0
        D = Vk**2 + 4 * pk * R_seg 
        
        if D < 0:
            return None  # Voltage Collapse: No steady-state solution
        
        # Physical solution using quadratic formula
        Vk1 = (Vk + np.sqrt(D)) / 2
        V.append(Vk1)
        
    return np.array(V)