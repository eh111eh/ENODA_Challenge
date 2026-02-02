import numpy as np
import matplotlib.pyplot as plt

def generate_stability_curve():
    # Parameters based on project assumptions
    Vk = 230.0  # Nominal Upstream Voltage
    R = 0.5     # Representative Line Resistance
    
    # Power loads (negative P) up to the theoretical limit
    # The limit is P = -V^2 / 4R
    p_limit = -Vk**2 / (4*R)
    P_range = np.linspace(p_limit, 0, 500)
    
    # Calculate downstream voltages using the positive root of the quadratic formula
    V_stable = []
    for p in P_range:
        # Discriminant check as performed in model.py
        D = Vk**2 + 4 * p * R
        V_stable.append((Vk + np.sqrt(D)) / 2)

    plt.figure(figsize=(9, 6))
    plt.plot(np.abs(P_range), V_stable, lw=3, color='#1f77b4', label='Stable Operating Region (D > 0)')
    
    # Highlight the Critical Point
    critical_p = np.abs(p_limit)
    critical_v = Vk / 2
    plt.scatter(critical_p, critical_v, color='red', s=100, zorder=5)
    
    # Add a vertical dashed line for the stability boundary
    plt.axvline(x=critical_p, color='gray', linestyle='--', alpha=0.5)
    
    # Modified Annotation with a descriptive box
    plt.annotate('STABILITY LIMIT\n(Voltage Collapse Point)', 
                 xy=(critical_p, critical_v), 
                 xytext=(critical_p * 0.5, critical_v - 40),
                 fontsize=10,
                 fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=1),
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2", color='black', lw=2))

    # Indicate the Infeasible Region (D < 0)
    plt.fill_between([critical_p, critical_p + 5000], 0, 250, color='red', alpha=0.1)
    plt.text(critical_p + 500, 100, 'INFEASIBLE REGION\n(D < 0)', color='red', fontsize=9, fontweight='bold', rotation=90)

    plt.title("Voltage Stability Analysis: Physical Meaning of the Discriminant", fontsize=12, pad=15)
    plt.xlabel("Total Downstream Power Demand |P| (Watts)", fontsize=11)
    plt.ylabel("Calculated Node Voltage V (Volts)", fontsize=11)
    plt.grid(True, which='both', linestyle=':', alpha=0.6)
    plt.legend(loc='upper right')
    
    # Set axis limits for clarity
    plt.xlim(0, critical_p + 4000)
    plt.ylim(0, 260)
    
    plt.tight_layout()
    plt.savefig("data/fig/voltage_collapse_theory.png")
    plt.show()

if __name__ == "__main__":
    generate_stability_curve()