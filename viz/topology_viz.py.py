import matplotlib.pyplot as plt
import networkx as nx

def generate_topology_comparison():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # --- Radial/Branched Network ---
    G_radial = nx.Graph()
    radial_edges = [(0,1), (1,2), (1,3), (2,4), (2,5), (3,6)]
    G_radial.add_edges_from(radial_edges)
    pos_radial = {0: (0, 1), 1: (1, 1), 2: (2, 1.5), 3: (2, 0.5), 4: (3, 1.8), 5: (3, 1.2), 6: (3, 0.5)}
    
    nx.draw(G_radial, pos_radial, ax=ax1, with_labels=False, node_color='skyblue', node_size=300)
    ax1.set_title("Actual Radial Topology\n(Complex Branching)")
    ax1.text(0, 0.8, "Substation", fontweight='bold')

    # --- Serial Approximation ---
    G_serial = nx.Graph()
    serial_edges = [(0,1), (1,2), (1,3), (3,4)]
    G_serial.add_edges_from(serial_edges)
    pos_serial = {0: (0, 0), 1: (1, 0), 2: (2, 0), 3: (3, 0), 4: (4, 0)}
    
    nx.draw(G_serial, pos_serial, ax=ax2, with_labels=False, node_color='lightgreen', node_size=300)
    ax2.set_title("Simplified Serial Model\n(Worst-Case Screening)")
    ax2.text(0, -0.2, "Substation", fontweight='bold')

    plt.tight_layout()
    plt.savefig("data/fig/topology_justification.png")
    plt.show()

if __name__ == "__main__":
    generate_topology_comparison()