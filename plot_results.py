import matplotlib.pyplot as plt
import pandas as pd
from simulate import calculate_voltage_profile

def main():
    top_10 = pd.read_csv("data/top_10_networks.csv")
    specs = pd.read_csv("data/network_specifications.csv", index_col="line")
    summer = pd.read_csv("data/summer_profile.csv", index_col=0)
    winter = pd.read_csv("data/winter_profile.csv", index_col=0)

    # Determine maximum available nodes from profile files
    max_nodes = len([c for c in summer.columns if c.startswith("p")])

    for _, row in top_10.iterrows():
        net_id = int(row["network_id"])
        N = int(row["size"])
        v0 = row["v0"]

        # Clip to available profile length
        N_use = min(N, max_nodes)

        Z = specs.loc[net_id, "line_impedance"] * specs.loc[net_id, "line_length"]

        available_cols = [c for c in summer.columns if c.startswith("p")]
        p_cols = [f"p{i}" for i in range(1, N + 1) if f"p{i}" in available_cols]
        p_s = summer.loc[net_id, p_cols].values
        p_w = winter.loc[net_id, p_cols].values

        v_s = calculate_voltage_profile(v0, Z, p_s)
        v_w = calculate_voltage_profile(v0, Z, p_w)

        plt.figure(figsize=(10, 6))
        plt.plot(v_s, label="Summer", lw=2)
        plt.plot(v_w, label="Winter", lw=2)
        plt.axhline(253, ls="--", color="red")
        plt.axhline(207, ls="--", color="red")
        plt.fill_between(range(len(v_s)), 207, 253, alpha=0.15)

        plt.title(f"Voltage Profile — Network {net_id}")
        plt.xlabel("Node index")
        plt.ylabel("Voltage (V)")
        plt.legend()
        plt.grid(alpha=0.3)

        plt.savefig(f"data/fig/plot_network_{net_id}.png")
        plt.close()

    print("Voltage plots generated.")

if __name__ == "__main__":
    main()
