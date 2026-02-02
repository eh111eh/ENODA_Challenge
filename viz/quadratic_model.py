import numpy as np
import matplotlib.pyplot as plt

# Color Palette Definitions
DARK_GREEN = '#229d45'
MID_GREEN = '#56b23f'
LIGHT_GREEN = '#7ed956'
DARK_GRAY = '#545454'
BLACK = '#000000'

# 1. Physics Parameters
V_nominal = 230  
R = 1.4          
P = np.linspace(0, 9500, 500)

# 2. Linear Model (Assuming constant current)
V_linear = V_nominal - (P/V_nominal) * R

# 3. Quadratic Model (Physical Reality)
discriminant = V_nominal**2 - 4 * P * R
P_quad = P[discriminant >= 0]
V_quad = (V_nominal + np.sqrt(V_nominal**2 - 4 * P_quad * R)) / 2
P_max = (V_nominal**2) / (4 * R)

# 4. Creating the Simplified Plot
plt.figure(figsize=(10, 6), facecolor='white')
ax = plt.gca()

# Plotting the lines
plt.plot(P, V_linear, color=MID_GREEN, linestyle='--', linewidth=2, label='Linear Approximation')
plt.plot(P_quad, V_quad, color=DARK_GREEN, linewidth=3.5, label='Quadratic Model')

# --- Vertical Dotted Line for Physical Limit ---
plt.axvline(x=P_max, color=BLACK, linestyle=':', linewidth=1.5, alpha=0.8)
# Adjusted text position to avoid overlap
plt.text(P_max + 150, 110, '', color=BLACK, rotation=90, 
         verticalalignment='bottom', horizontalalignment='left', fontweight='bold')

# --- Highlight the Collapse Point ---
plt.scatter(P_max, V_nominal/2, color=BLACK, s=120, zorder=5)

# FIXED: Adjusted 'xytext' and alignment to prevent overlapping with letters or lines
plt.annotate('VOLTAGE COLLAPSE', 
             xy=(P_max, V_nominal/2), 
             xytext=(P_max - 500, V_nominal/2 - 40), # Moved further down and right
             ha='right', # Horizontal alignment right to keep text away from the line
             arrowprops=dict(arrowstyle='->', color=BLACK, lw=1.5, connectionstyle="arc3,rad=.2"),
             fontsize=10, fontweight='bold', color=BLACK)

# Statutory Limit Line (Horizontal)
plt.axhline(y=207, color=DARK_GRAY, linestyle=':', linewidth=1)
plt.text(500, 210, 'Statutory Limit (207V)', color=DARK_GRAY, fontsize=9)

# Formatting for Slide Aesthetic
plt.title('Nonlinear Quadratic Model', 
          fontsize=16, fontweight='bold', color=BLACK, pad=20)
plt.xlabel('Power Demand (Watts)', fontsize=12, color=DARK_GRAY)
plt.ylabel('Node Voltage (Volts)', fontsize=12, color=DARK_GRAY)

# Clean up axes
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(DARK_GRAY)
ax.spines['bottom'].set_color(DARK_GRAY)

plt.xlim(0, 11500) # Increased x-limit slightly to fit the vertical text
plt.ylim(100, 240)
plt.grid(axis='y', linestyle='-', alpha=0.1)
plt.legend(frameon=False, loc='lower left', fontsize=11)

plt.tight_layout()
plt.show()