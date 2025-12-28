import numpy as np

# -------------------------------
# Voltage limits
# -------------------------------
V_NOMINAL = 230.0
V_MIN = 207.0
V_MAX = 253.0

def calculate_voltage_profile(v0, Z, p_values):
    """
    Compute node voltages along a serial network using full downstream power.

    Parameters
    ----------
    v0 : float
        Substation voltage (secondary side)
    Z : float
        Line impedance per segment (Ohms)
    p_values : array-like
        Power injections at nodes (W). Negative for load, positive for generation.

    Returns
    -------
    numpy.ndarray
        Voltages at all nodes including substation [v0 ... vN]
    """
    N = len(p_values)
    v = np.zeros(N + 1)
    v[0] = v0

    # Compute total downstream power at each segment
    p_downstream = np.cumsum(p_values[::-1])[::-1]  # sum from node i to end

    for i in range(1, N + 1):
        # Convert to kW
        p_kw = p_downstream[i - 1] * 1e-3

        # Voltage drop approximation: ΔV = Z * I ~ Z * P / V
        delta_v = Z * p_kw / v[i - 1]

        # Subtract for consumption, add for generation
        v[i] = v[i - 1] - delta_v

    return v

def within_statutory_limits(v_profile):
    """
    Check if all node voltages are within statutory limits.
    """
    return np.all((v_profile >= V_MIN) & (v_profile <= V_MAX))

def voltage_margin(v_profile):
    """
    Compute margin: minimum distance to voltage limits.
    Positive if safely within limits, negative if violating.
    """
    return min(v_profile - V_MIN.min(), V_MAX.max() - v_profile.max())
