import numpy as np
import pandas as pd
from simulate import calculate_voltage_profile, within_statutory_limits

# Transformer regulation bounds (±5%)
V0_MIN = 219.0
V0_MAX = 242.0

def find_feasible_setpoint(Z, p_summer, p_winter):
    """
    Find feasible substation voltage v0 that satisfies voltage limits
    for both summer and winter profiles.
    Returns: feasible (bool), best_v0 (float), effort (float)
    """
    v0_candidates = np.linspace(V0_MIN, V0_MAX, 47)
    feasible_setpoints = []

    for v0 in v0_candidates:
        v_s = calculate_voltage_profile(v0, Z, p_summer)
        v_w = calculate_voltage_profile(v0, Z, p_winter)

        if within_statutory_limits(v_s) and within_statutory_limits(v_w):
            feasible_setpoints.append(v0)

    if not feasible_setpoints:
        return False, None, None

    # Choose setpoint closest to nominal voltage
    best_v0 = min(feasible_setpoints, key=lambda x: abs(x - 230.0))

    # Compute maximum deviation along network as effort
    v_s = calculate_voltage_profile(best_v0, Z, p_summer)
    v_w = calculate_voltage_profile(best_v0, Z, p_winter)
    effort = max(
        max(abs(v_s - 230.0)),
        max(abs(v_w - 230.0))
    )

    return True, best_v0, effort

def main():
    # Load CSVs
    specs = pd.read_csv("data/network_specifications.csv", index_col="line")
    summer = pd.read_csv("data/summer_profile.csv", index_col=0)
    winter = pd.read_csv("data/winter_profile.csv", index_col=0)

    # Keep only networks present in both profile files
    specs = specs[specs.index.isin(summer.index) & specs.index.isin(winter.index)]

    results = []

    for net_id, row in specs.iterrows():
        N = int(row["size"])
        Z = row["line_impedance"] * row["line_length"]

        # Ensure we don't request more nodes than available in profiles
        N_summer = min(N, len([c for c in summer.columns if c.startswith("p")]) - 1)
        N_winter = min(N, len([c for c in winter.columns if c.startswith("p")]) - 1)

        p_cols_s = [f"p{i}" for i in range(1, N_summer + 1)]
        p_cols_w = [f"p{i}" for i in range(1, N_winter + 1)]

        p_s = summer.loc[net_id, p_cols_s].values
        p_w = winter.loc[net_id, p_cols_w].values

        if np.isnan(p_s).any() or np.isnan(p_w).any():
            continue

        feasible, v0, effort = find_feasible_setpoint(Z, p_s, p_w)
        if feasible:
            results.append({
                "network_id": net_id,
                "size": N,
                "v0": v0,
                "effort": effort
            })

    if not results:
        raise RuntimeError(
            "No feasible networks found. Check CSV data and voltage model."
        )

    # Rank by largest network first, then lowest effort
    df = pd.DataFrame(results)
    df = df.sort_values(by=["size", "effort"], ascending=[False, True]).head(10)
    df.to_csv("top_10_networks.csv", index=False)

    print("\nSelected Top 10 Networks:\n")
    print(df)

if __name__ == "__main__":
    main()
