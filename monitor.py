import os
import numpy as np
from data_packet import DataPacket
import pandas as pd
from field_mappings import *
from pcap_parser import *


# TODO: add rate gap
def evaluate_throughput_list(packets: list[DataPacket]):
    throughput_arr = np.empty(len(packets), dtype=float)
    timestamps = np.empty(len(packets), dtype=float)
    retransmits = 0
    for i, packet in enumerate(packets):
        if packet.retry:
            retransmits += 1
        frame_loss_rate = retransmits / (i + 1)

        timestamps[i] = packet.timestamp
        throughput_arr[i] = float(packet.data_rate) * (1.0 - frame_loss_rate)

    return timestamps, throughput_arr


def evaluate_throughput_df(df: pd.DataFrame):
    retransmits = df["retry"].cumsum().values
    frame_loss_rate = retransmits / np.arange(1, len(df) + 1)
    throughput_arr = df["data_rate"].values * (1.0 - frame_loss_rate)
    df["throughput"] = throughput_arr

    # df.to_csv("./data/throughput.csv", index=False)


"""
    Monitoring 1.1: Network Density
    This function uses the RSSID metric referenced in the paper:
        Pefkianakis et al. “Characterizing Home Wireless Performance: The Gateway View”, IEEE INFOCOM 2015 
"""


def aggregate_beacon_packets(network_files):
    os.makedirs(f"./data/aggregates", exist_ok=True)
    for network_name in network_files:
        df = pd.read_csv(f"./data/parsed/{network_name}.csv")

        # group by ssid, rssi and primary channel, count occurences
        df = df.groupby(["ssid", "rssi", "channel"]).size().reset_index(name="count")

        # group by ssid and channel to get rssi based on max occurences
        df = df.groupby(["ssid", "channel"]).max("count")
        df = df.drop("count", axis=1)
        df.to_csv(f"./data/aggregates/agg_{network_name}.csv")


def monitor_network_density(network_files):
    results = []
    for network_name in network_files:
        df = pd.read_csv(f"./data/aggregates/agg_{network_name}.csv")
        RSSID = (1 / abs(df["rssi"])).sum()

        results.append({"Network": network_name, "Density": RSSID})

    result_df = pd.DataFrame(results)
    result_df.to_csv("./output/network_density_metrics.csv", index=True)
