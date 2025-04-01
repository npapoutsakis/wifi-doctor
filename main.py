# WiFi Doctor - Networks 2025

# Group 4:
#       - Nikolaos Papoutsakis  2019030206
#       - Argyris Christakis    2019030078
#       - Michalis Syrianos     2019030058
#       - Swkratis Siganos      2019030097


"""
This will be the main file that will run the whole project.
    1. Network Sniffing
    2. Pcap Parsing
    3. Performance Monitoring
    4. Performance Analysis
    5. Visualization
"""

from analyzer import *
from field_mappings import *
import pandas as pd
import numpy as np
import glob  # used for file globbing :) [*.pcap]
from pcap_parser import *
from monitor import *
from visualizer import *
import matplotlib.pyplot as plt


AP_MAC = "2C:F8:9B:DD:06:A0"
DEV_MAC = "00:20:A6:FC:B0:36"
PCAP_HOW = "./pcaps/HowIWiFi_PCAP.pcap"

"""
    Scenario 1.1: WiFi Network Density
"""


def network_density():

    networks = ["home-2ghz", "tuc-2ghz", "home-5ghz", "tuc-5ghz"]

    ### PARSER
    for network in networks:
        pcaps = glob.glob(f"./beacon_pcaps/{network}/*.pcap")
        parse_network_beacon_pcaps(pcaps, network)

    ### MONITOR - aggregate data and calculate network density
    aggregate_beacon_packets(networks)
    monitor_network_density(networks)

    ### VISUALIZER
    for network in networks:
        is_5ghz = "5ghz" in network
        df = pd.read_csv(f"./data/aggregates/agg_{network}.csv")
        plot_network_density_figures(df, network, is_5ghz)


def data_analyze(network: str):

    ### Create Data
    df = data_parser(PCAP_HOW, AP_MAC, DEV_MAC)
    evaluate_throughput_df(df)
    add_rate_gap_to_df(df)
    df.to_csv("./data/how.csv", index=False)

    df = pd.read_csv(f"./data/how.csv")

    ### Save Data?

    ### Visualize Data

    # plot rssi vs phytype an allazei
    # plot rssi vs rategap gia megali apostasi
    # plot bandwidth vs rssi? gia 5ghz >bandwidth, isos otan peftei rssi peftei bandiwdth?

    plot_network_performance_figures(df, network)
    export_statistics(df, network)


def main():
    data_analyze("HOW")
    network_density()


if __name__ == "__main__":
    main()
