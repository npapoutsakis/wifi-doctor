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


def evaluate_throughput_df(packets_df: pd.DataFrame):
    retransmits = packets_df["retry"].cumsum()
    frame_loss_rate = retransmits / np.arange(1, len(packets_df) + 1)

    throughput_arr = packets_df["data_rate"].values * (1.0 - frame_loss_rate)
    # packets_df.to_csv("./data/throughput.csv", index=False)

    return throughput_arr


"""
    Monitoring 1.1: Network Density
    This function uses the RSSID metric referenced in the paper:
        Pefkianakis et al. “Characterizing Home Wireless Performance: The Gateway View”, IEEE INFOCOM 2015 
"""


def monitor_1_1(network_files):
    results = []
    for network_name, network_file in network_files.items():
        df = pd.read_csv(network_file)

        # group by SSID and RSSI(dBm) and count the occurrences
        result = df.groupby(["SSID", "RSSI(dBm)"]).size().reset_index(name="count")

        # find the max of each ssid
        max_entries_per_ssid = result.loc[result.groupby("SSID")["count"].idxmax()]

        # Calculate RSSID metric
        RSSID = (1 / abs(max_entries_per_ssid["RSSI(dBm)"])).sum()

        results.append({"Network": network_name, "Density": RSSID})

    result_df = pd.DataFrame(results)
    result_df.to_csv("./output/network_density_metrics.csv", index=True)
    # print(result_df)
