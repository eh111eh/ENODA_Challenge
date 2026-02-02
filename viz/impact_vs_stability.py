import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# 1. Load the top 10 networks data
top_10 = pd.read_csv('data/top_10_networks.csv')

# 2. Configure the plot
plt.figure(figsize=(12, 7))

# Define colors based on robustness
# Robust networks (Green) vs non-robust (Red)
colors = ['#27ae60' if robust else '#e74c3c' for robust in top_10['is_robust']]
sizes = top_10['size_N'] * 15  # Scale point size by number of customers

# 3. Create Scatter Plot: Size (N) vs. Safety Margin
plt.scatter(
    top_10['size_N'], 
    top_10['avg_safety_margin'], 
    s=sizes, 
    c=colors, 
    alpha=0.7, 
    edgecolors='k', 
    linewidth=1
)

# 4. Highlight the "Feasibility Gate" for Site 9832
site_9832 = top_10[top_10['network_id'] == 9832].iloc[0]
plt.annotate(
    f'Feasibility Gate: ID 9832\n(Size N=90)\nMargin: {site_9832["avg_safety_margin"]:.2f}V',
    xy=(site_9832['size_N'], site_9832['avg_safety_margin']),
    xytext=(site_9832['size_N'] - 15, site_9832['avg_safety_margin'] + 1.5),
    arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=8),
    fontsize=11,
    fontweight='bold',
    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.9)
)

# 5. Add Reference Line for Voltage Collapse Point
plt.axhline(y=0, color='#c0392b', linestyle='--', linewidth=2)
plt.fill_between([top_10['size_N'].min()-5, top_10['size_N'].max()+5], -1, 0, color='#e74c3c', alpha=0.1)
plt.text(top_10['size_N'].min() - 2, -0.6, 'VOLTAGE COLLAPSE ZONE', color='#c0392b', fontweight='bold')

# 6. Formatting
plt.title('Impact vs. Physical Stability: Reach vs. Resilience', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Impact: Network Size (Number of Nodes $N$)', fontsize=13)
plt.ylabel('Resilience: Avg. Voltage Safety Margin (V)', fontsize=13)
plt.xlim(top_10['size_N'].min() - 5, top_10['size_N'].max() + 5)
plt.ylim(-1, top_10['avg_safety_margin'].max() + 3)
plt.grid(True, linestyle='--', alpha=0.6)

# Legend
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Robust (Passed 10% Stress)',
           markerfacecolor='#27ae60', markersize=12),
    Line2D([0], [0], marker='o', color='w', label='Sensitive (Baseline Only)',
           markerfacecolor='#e74c3c', markersize=12),
    Line2D([0], [0], color='#c0392b', linestyle='--', label='Stability Limit (D=0)')
]
plt.legend(handles=legend_elements, loc='upper left', frameon=True, fontsize=11)

plt.tight_layout()
plt.savefig('data/fig/impact_vs_stability.png', dpi=300)