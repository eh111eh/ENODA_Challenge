import matplotlib.pyplot as plt
from model import V_MIN, V_MAX

def plot_voltage_profile(network_id, V_winter, V_summer):
    """Generates a voltage profile graph for the report."""
    plt.figure(figsize=(10, 5))
    plt.axhline(y=V_MAX, color='red', linestyle='--', label='Statutory Max (253V)')
    plt.axhline(y=V_MIN, color='red', linestyle='--', label='Statutory Min (207V)')
    
    if V_winter is not None:
        plt.plot(V_winter, 'b-o', label='Peak Winter Profile')
    if V_summer is not None:
        plt.plot(V_summer, 'g-s', label='Peak Summer Profile')
        
    plt.title(f"Voltage Profile: Network {network_id}")
    plt.xlabel("Node Index")
    plt.ylabel("Voltage (V)")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"data/fig/network_{network_id}_profile.png")
    plt.close()