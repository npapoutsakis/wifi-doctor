import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd
import seaborn as sns
import numpy as np
from data_packet import DataPacket
from field_mappings import *
from helper import CHANNELS_5GHZ

"""
    Network Performance Visualizer
"""


# def plot_throughput(t, data):
#     plt.figure()
#     plt.plot(t, data)
#     plt.grid(True)
#     plt.ylabel("Downlink Throughput (Mbps)")
#     plt.xlabel("Time (s)")
#     return


def plot_throughput_df(df: pd.DataFrame):
    # t = np.array([pkt.timestamp for pkt in data])
    # thresholds = [0, 25, 75, 150, 250, max(throughput) + 50] # keep???
    fig = plt.figure()
    plt.plot(df["timestamp"].values, df["throughput"].values)
    plt.grid(True)
    plt.ylabel("Throughput (Mbps)")
    plt.xlabel("Time (s)")
    # plt.tight_layout()
    # plt.show()
    return fig


# TODO: Idea, when i do the capture where as time passes i move further and further from the ap
# then i plot rssi vs throughput and i see that when rssi drops, throughput goes down
def plot_rssi_vs_throughput(df: pd.DataFrame):
    fig = plt.figure()
    plt.scatter(df["throughput"].values, df["rssi"].values)
    plt.xlabel("Throughput (Mbps)")
    plt.ylabel("RSSI (dBm)")
    return fig


def plot_rssi_vs_short_gi(df: pd.DataFrame):
    fig = plt.figure(figsize=(8, 6))
    sns.countplot(x="rssi", hue="short_gi", data=df, palette=["C0", "C1"])
    plt.xlabel("RSSI (dBm)")
    plt.ylabel("Count")
    plt.title("RSSI vs Short Guard Interval")
    plt.legend(title="Short Guard Interval", loc="upper right")
    return fig


def plot_rssi_vs_bandwidth(df: pd.DataFrame):
    fig = plt.figure(figsize=(8, 6))
    bandwidth_col = df["bandwidth"].map(lambda x: bandwidth_mapping[x])

    sns.countplot(x=df["rssi"], hue=bandwidth_col)
    plt.xlabel("RSSI (dBm)")
    plt.ylabel("Count")
    plt.title("RSSI vs Bandwidth")
    plt.legend(title="Bandwidth", loc="upper right")
    return fig


def plot_rate_gap(df: pd.DataFrame):

    t = df["timestamp"].values
    data = df["rate_gap"].values

    # Get indices and values where index != 0
    non_zero_mask = data != 0
    non_zero_times = t[non_zero_mask]
    non_zero_values = data[non_zero_mask]

    min = non_zero_values.min()
    max = non_zero_values.max()

    # Plot
    fig = plt.figure()
    plt.scatter(
        non_zero_times,
        non_zero_values,
        marker="o",
        c=non_zero_values,
        s=10,
        cmap="viridis",
    )
    # plt.colorbar(label="Rate Gap Value")
    plt.yticks(np.arange(min, max + 1))
    plt.ylim(min - 0.5, max + 0.5)
    plt.xlabel("Time (s)")
    plt.ylabel("Rate Gap (MCS)")
    # plt.title("Non-Zero Rate Gaps Over Time")
    plt.grid(alpha=0.3)

    return fig


def plot_network_performance_figures(df: pd.DataFrame, folder_name: str):
    folder_path = f"./figures/{folder_name}"
    os.makedirs(f"{folder_path}", exist_ok=True)

    fig = plot_throughput_df(df)
    fig.savefig(f"{folder_path}/{folder_name}_throughput.png")

    fig = plot_rssi_vs_throughput(df)
    fig.savefig(f"{folder_path}/{folder_name}_rssi_vs_throughput.png")

    fig = plot_rate_gap(df)
    fig.savefig(f"{folder_path}/{folder_name}_rate_gap.png")

    fig = plot_rssi_vs_short_gi(df)
    fig.savefig(f"{folder_path}/{folder_name}_rssi_vs_short_gi.png")

    fig = plot_rssi_vs_bandwidth(df)
    fig.savefig(f"{folder_path}/{folder_name}_rssi_vs_bandwidth.png")


"""
    Network Density Visualizer
"""


def plot_rssi_vs_channels_occupancy(df: pd.DataFrame, network_name, is_5ghz):
    # Get saturated colors for better visibility
    if is_5ghz:
        columns = CHANNELS_5GHZ
    else:
        columns = range(1, 14)

    # Create plot
    fig = plt.figure()

    # Create the heatmap

    sns.set_style("white")

    df = df.pivot_table(index="rssi", columns="channel", aggfunc="size")
    df = df.reindex(columns=columns, fill_value=np.nan)

    vmin = df.min().min()
    vmax = df.max().max()

    g = sns.heatmap(
        df,
        cmap="viridis",
        cbar_kws={"shrink": 0.5},
        robust=True,
        square=True,
        linewidths=0.5,
        linecolor="black",
        vmin=vmin,
        vmax=vmax,
        rasterized=True,
        xticklabels=columns,
    )

    g.set_ylabel("RSSI (dBm)")
    g.set_xlabel("Channel")
    g.invert_yaxis()

    # Add title
    plt.title(f"{network_name} Network Density")

    plt.tight_layout()

    return fig


def plot_network_density_figures(df: pd.DataFrame, network_name: str, is_5ghz: bool):
    folder_path = f"./figures/density/{network_name}"
    os.makedirs(f"{folder_path}", exist_ok=True)

    fig = plot_rssi_vs_channels_occupancy(df, network_name, is_5ghz)
    fig.savefig(f"{folder_path}/{network_name}_occupancy.png")
