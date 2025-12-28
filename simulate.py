import numpy as np

# -------------------------------
# Voltage limits
# -------------------------------
V_NOMINAL = 230.0
V_MIN = 207.0
V_MAX = 253.0

# -------------------------------
# Transformer regulation / load diversity
# -------------------------------
LOAD_DIVERSITY = 0.05  # non-coincident peak factor

def calculate_voltage_profile(v0, Z, p_values):
    """
    Serial LV network voltage calculation using cumulative downstream power.

    Parameters
    ----------
    v0 : float
        Substation voltage (V)
    Z : float
        Line impedance per segment (Ohm)
    p_values : array-like
        Power injections at each node (W). Positive = generation, negative = load

    Returns
    -------
    v : np.ndarray
        Voltages at all nodes, v[0] = v0
    """
    N = len(p_values)
    v = np.zeros(N + 1)
    v[0] = v0

    # Compute cumulative downstream power (including this node)
    p_downstream = np.cumsum(p_values[::-1])[::-1]

    for i in range(1, N + 1):
        # Apply diversity factor and convert to kW
        p_kw = LOAD_DIVERSITY * p_downstream[i - 1] * 1e-3

        # Avoid division by zero in rare cases
        if v[i - 1] <= 0:
            v[i:] = 0
            break

        # Voltage drop: ΔV = Z * I, I = P / V
        delta_v = Z * p_kw / v[i - 1]

        # Sending -> receiving voltage
        v[i] = v[i - 1] - delta_v

    return v


def within_statutory_limits(v_profile):
    """
    Checks if all node voltages are within statutory limits.
    """
    return np.all((v_profile >= V_MIN) & (v_profile <= V_MAX))
