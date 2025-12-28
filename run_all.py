import rank_networks
import robustness
import plot_results

if __name__ == "__main__":
    print("=== STAGE 1: NETWORK SELECTION ===")
    rank_networks.main()

    # print("\n=== STAGE 2: ROBUSTNESS ANALYSIS ===")
    # robustness.main()

    # print("\n=== VISUALIZATION ===")
    # plot_results.main()

    # print("\nChallenge pipeline completed successfully.")
