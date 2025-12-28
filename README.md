# ENODA_Challenge
A power system simulation and optimization pipeline designed to identify the 10 most suitable distribution networks for the installation of a substation voltage regulation device.

## Project Overview
The objective is to screen 20,000 candidate Low-Voltage (LV) distribution networks. Each network is modeled as a serial distribution line where the goal is to maintain all customer node voltages within statutory limits ($207\text{V}$ to $253\text{V}$) under peak summer (high solar generation) and peak winter (high load) conditions.

The project follows a two-stage selection process:

1. **Stage 1: Technical Feasibility & Ranking:** Identify networks that can be successfully regulated and rank them by size ($N$) and efficiency.

2. **Stage 2: Robustness Analysis:** Stress-test the top selections against a $30\%$ load increase to ensure long-term operational resilience.

## Repository Structure
- `simulate.py`: The core physics engine. It implements the recursive voltage calculation for serial networks, accounting for line impedance and downstream power flows.

- `rank_networks.py`: Performs the initial screening. It iterates through all candidates and finds an optimal substation setpoint ($V_0$) within the $\pm 5\%$ regulation band.

- `robustness.py`: Re-evaluates the top 10 candidates under a "High Stress" scenario ($+30\%$ load) to quantify confidence in the selection.

- `plot_results.py`: Generates voltage profile charts for the final selections, showing the voltage at every node along the line for both seasons.