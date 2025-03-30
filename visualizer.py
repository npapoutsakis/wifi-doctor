import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd
import seaborn as sns
import numpy as np
from data_packet import DataPacket
from field_mappings import *

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
    plt.title("RSSI vs Short Guard Interval")
    plt.legend(title="Short Guard Interval", loc="upper right")
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


def plot_channel_occupancy_by_ssid(df):
    # Group data by CHANNEL and SSID and count the occurrences
    channel_ssid_counts = df.groupby(["CHANNEL", "SSID"]).size().unstack(fill_value=0)

    # Generate a color palette for each SSID
    ssid_colors = sns.color_palette("tab20", len(channel_ssid_counts.columns))

    fig = plt.figure()

    # Plot channel occupancy with different colors for SSIDs
    ax = channel_ssid_counts.plot(
        kind="bar", stacked=True, figsize=(12, 7), color=ssid_colors, edgecolor="black"
    )

    # Adding labels and title
    plt.title("Channel Occupancy by SSID", fontsize=14)
    plt.xlabel("Channel", fontsize=12)
    plt.ylabel("Number of Beacons", fontsize=12)
    plt.xticks(rotation=0)  # Rotate x-axis labels to make them horizontal
    plt.legend(title="SSID", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()

    return fig


def plot_rssi_vs_frequency(df):
    channel_ssid_rssi = (
        df.groupby(["channel", "ssid"])["rssi"].mean().unstack(fill_value=0)
    )

    # Get saturated colors for better visibility
    ssid_colors = sns.color_palette("tab20", len(channel_ssid_rssi.columns))

    # Set transparency range (more opaque than before)
    alpha_values = np.linspace(0.7, 0.95, len(channel_ssid_rssi.columns))

    # Create plot
    fig = plt.figure(figsize=(14, 7))
    legend_handles = []

    # Plot each SSID and channel
    for i, ssid in enumerate(channel_ssid_rssi.columns):
        for channel in channel_ssid_rssi.index:
            # TODO: Ftiakse to bandwidth
            bandwidth = channel_to_bandwidth_2_4_ghz[channel]
            rssi_value = channel_ssid_rssi.loc[channel, ssid]
            if rssi_value == 0:
                print(f"SSID: {ssid} Channel: {channel} RSSI: {rssi_value}")

            width = bandwidth / 5  # 20MHz width = 4 channel units

            plt.bar(
                channel,
                rssi_value + 90,
                width=width * 0.9,
                color=ssid_colors[i],
                alpha=0.3,
                edgecolor="black",
                bottom=-90,
            )

        legend_handles.append(Line2D([0], [0], color=ssid_colors[i], lw=4, label=ssid))

    # Configure axes with INVERTED Y-AXIS
    plt.xticks(range(1, 14))
    plt.yticks(range(-90, 31, 10))
    plt.ylim(-90, 30)
    # plt.gca().invert_yaxis()  # This line flips the y-axis

    # Add labels and title
    plt.title("Wi-Fi Signal Strength by Channel", fontsize=14)
    plt.xlabel("Channel", fontsize=12)
    plt.ylabel("Signal Strength (dBm)", fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Add legend
    plt.legend(
        handles=legend_handles, title="SSID", bbox_to_anchor=(1.05, 1), loc="upper left"
    )

    plt.tight_layout()

    return fig


def plot_network_density_figures(df: pd.DataFrame, folder_name: str):
    folder_path = f"./figures/density/{folder_name}"
    os.makedirs(f"{folder_path}", exist_ok=True)

    # fig = plot_channel_occupancy_by_ssid(df)
    # fig.savefig(f"{folder_path}/{folder_name}_occupancy.png")

    fig = plot_rssi_vs_frequency(df)
    fig.savefig(f"{folder_path}/{folder_name}_rssi_vs_frequency.png")
