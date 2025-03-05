import matplotlib.pyplot as plt
import plotly.graph_objects as go
import os


def plot_optimal_profit(results):
    """
    Plots Optimal Profit vs. Truck Capacity.
    
    :param results list with list of truck capacities and a list of optimal profits corresponding to each capacity.
    """

    fig = plt.figure(figsize=(10, 6))
    capacities_plot, objectives = zip(*results)
    plt.plot(capacities_plot, objectives, marker='o', linestyle='-', color='#ffe600', markerfacecolor='#ffe600')
    plt.xlabel("Truck Capacity")
    plt.ylabel("Optimal Profit")
    plt.title("Optimal Profit vs. Truck Capacity")
    plt.grid(True)
    plt.show()

    fig.savefig("../../plots/optimal_profit_vs_truck_capacity.png", dpi=330)


def plot_interative_optimal_profit(results):
    """
    Plots Optimal Profit vs. Truck Capacity using Plotly and saves it as an interactive HTML file.
    
    :param results list with list of truck capacities and a list of optimal profits corresponding to each capacity.
    """

    save_path="../../plots/"

    capacities_plot, objectives = zip(*results)  # Extract data

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=capacities_plot,
        y=objectives,
        mode='lines+markers',
        marker=dict(size=8, color='blue'),
        line=dict(width=2)
    ))

    fig.update_layout(
        title="Optimal Profit vs. Truck Capacity",
        xaxis_title="Truck Capacity",
        yaxis_title="Optimal Profit",
        template="plotly_white"
    )

    try:
        fig.write_html(save_path)
        print(f"Plot saved successfully at {save_path}")
    except PermissionError:
        print(f"PermissionError: Could not save file to {save_path}. Try changing the save path.")
    except Exception as e:
        print(f"Unexpected error: {e}")

    fig.show()


def plot_fitness_history(fitness_history):
    plt.figure(figsize=(8, 5))
    plt.plot(range(len(fitness_history)), fitness_history, marker='o', linestyle='-')
    plt.title("Best Raw Fitness per Generation (Shifted for Selection)")
    plt.xlabel("Generation")
    plt.ylabel("Best Raw Fitness")
    plt.grid(True)
    plt.show()