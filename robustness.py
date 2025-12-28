import pandas as pd
from rank_networks import find_feasible_setpoint

LOAD_STRESS = 1.30  # +30%

def main():
    top_10 = pd.read_csv("data/top_10_networks.csv")
    specs = pd.read_csv("data/network_specifications.csv", index_col="line")
    summer = pd.read_csv("data/summer_profile.csv", index_col=0)
    winter = pd.read_csv("data/winter_profile.csv", index_col=0)

    # Maximum usable nodes (p1 ... pN, no p0)
    max_nodes = len([c for c in summer.columns if c.startswith("p")]) - 1

    results = []

    for _, row in top_10.iterrows():
        net_id = int(row["network_id"])
        N = int(row["size"])

        # Clip to available profile length
        N_use = min(N, max_nodes)

        Z = specs.loc[net_id, "line_impedance"] * specs.loc[net_id, "line_length"]

        p_cols = [f"p{i}" for i in range(1, N_use + 1)]

        p_s = summer.loc[net_id, p_cols].values * LOAD_STRESS
        p_w = winter.loc[net_id, p_cols].values * LOAD_STRESS

        feasible, v0, effort = find_feasible_setpoint(Z, p_s, p_w)

        results.append({
            "network_id": net_id,
            "status": "ROBUST" if feasible else "SENSITIVE",
            "v0_stressed": v0,
            "effort_stressed": effort
        })

    df = pd.DataFrame(results)
    df.to_csv("data/robustness_report.csv", index=False)

    print("\nRobustness Results:\n")
    print(df)

if __name__ == "__main__":
    main()
