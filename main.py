import pandas as pd
import numpy as np
from model import compute_voltages, V_NOMINAL
from screening import is_feasible
from robustness import stress_profile, calculate_safety_margin
from visualization import plot_voltage_profile

# 1. Load Data
networks = pd.read_csv("data/network_specifications.csv")
winter = pd.read_csv("data/winter_profile.csv")
summer = pd.read_csv("data/summer_profile.csv")

results = []

# 2. Screening and Selection
for idx, row in networks.iterrows():
    N = int(row["size"])
    R_seg = row["line_impedance"] * row["line_length"]
    
    # Extract profiles (excluding p0/secondary bus which is always 0)
    Pw = winter.iloc[idx, 2:N+1].values 
    Ps = summer.iloc[idx, 2:N+1].values

    V0w = is_feasible(Pw, R_seg)
    V0s = is_feasible(Ps, R_seg)

    if V0w is None or V0s is None: continue

    # Robustness and Margin calculations
    robust = (is_feasible(stress_profile(Pw), R_seg) is not None and 
              is_feasible(stress_profile(Ps), R_seg) is not None)
    
    Vw = compute_voltages(V0w, Pw, R_seg)
    Vs = compute_voltages(V0s, Ps, R_seg)
    
    margin_w = calculate_safety_margin(Vw)
    margin_s = calculate_safety_margin(Vs)
    effort = (abs(V0w - V_NOMINAL) + abs(V0s - V_NOMINAL)) / 2

    results.append({
        "network_id": idx,
        "size_N": N,
        "is_robust": robust,
        "avg_safety_margin": (margin_w + margin_s) / 2,
        "reg_effort_V": round(effort, 2),
        "V0_winter": round(V0w, 2),
        "V0_summer": round(V0s, 2),
        "min_V_winter": round(np.min(Vw), 2),
        "max_V_summer": round(np.max(Vs), 2),
        "Vw_array": Vw, "Vs_array": Vs # For plotting
    })

# 3. Final Ranking and CSV Export
df_results = pd.DataFrame(results)
top10 = df_results.sort_values(
    by=["size_N", "is_robust", "avg_safety_margin"], 
    ascending=[False, False, False]
).head(10)

# Save statistics to CSV 
top10.drop(columns=["Vw_array", "Vs_array"]).to_csv("data/top_10_networks.csv", index=False)

# 4. Generate Visualizations for Top 10
for _, winner in top10.iterrows():
    plot_voltage_profile(winner['network_id'], winner['Vw_array'], winner['Vs_array'])

print("Top 10 networks identified and exported to top_10_networks.csv.")