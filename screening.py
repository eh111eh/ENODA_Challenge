import numpy as np
from model import compute_voltages, V_MIN, V_MAX, V_NOMINAL

# Substation Control Range: +/- 5% of nominal 
V0_MIN = 218.5
V0_MAX = 241.5

def is_feasible(P_injections, R_seg):
    """
    Finds the V0 in [V0_MIN, V0_MAX] that minimizes |V0 - 230| 
    while keeping all nodes within statutory limits.
    """
    best_V0 = None
    min_effort = float('inf')

    # Iterate through potential substation set-points
    for v_test in np.linspace(V0_MIN, V0_MAX, 47): # 0.5V steps
        V = compute_voltages(v_test, P_injections, R_seg)
        
        if V is not None:
            # Check statutory compliance: 207V <= Vi <= 253V
            if np.all(V >= V_MIN) and np.all(V <= V_MAX):
                effort = abs(v_test - V_NOMINAL)
                if effort < min_effort:
                    min_effort = effort
                    best_V0 = v_test
                    
    return best_V0