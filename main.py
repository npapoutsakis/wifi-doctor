# WiFi Doctor - Networks 2025

# Group 4:
#       - Nikolaos Papoutsakis  2019030206
#       - Argyris Christakis    2019030078
#       - Michalis Syrianos     2019030058
#       - Sokratis Siganos      2019030097


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


# AP_MAC = "2C:F8:9B:DD:06:A0"
# DEV_MAC = "00:20:A6:FC:B0:36"
PCAP_HOW = "./data_pcaps/HowIWiFi_PCAP.pcap"


TA_MAC_2 = "F8:AA:3F:6D:02:B6"
TA_MAC_5 = "F8:AA:3F:6D:02:BB"
RA_MAC = "f4:02:28:d6:f4:f8"

THR_2GHZ_1M = "./data_pcaps/2ghz_1m.pcap"
THR_2GHZ_10M = "./data_pcaps/2ghz_10m.pcap"
THR_2GHZ_MOVING = "./data_pcaps/2ghz_moving.pcap"
THR_5GHZ_1M = "./data_pcaps/5ghz_1m.pcap"
THR_5GHZ_10M = "./data_pcaps/5ghz_10m.pcap"
THR_5GHZ_MOVING = "./data_pcaps/5ghz_moving.pcap"


"""
    Scenario 1.1: WiFi Network Density
"""


def network_density():

    networks = ["home-2ghz", "tuc-2ghz", "home-5ghz", "tuc-5ghz"]

    # !Disabled parser since .zip doesn't contain beacon pcaps due to size.
    # Insert pcaps in beacon_pcaps/{network_name}/*.pcap for beacon packet analysis
    # Insert network_name in list above

    ### PARSER
    # for network in networks:
    #     pcaps = glob.glob(f"./beacon_pcaps/{network}/*.pcap")
    #     parse_network_beacon_pcaps(pcaps, network)

    ### MONITOR - aggregate data and calculate network density
    aggregate_beacon_packets(networks)
    monitor_network_density(networks)

    ### VISUALIZER
    for network in networks:
        is_5ghz = "5ghz" in network
        df = pd.read_csv(f"./data/aggregates/agg_{network}.csv")
        plot_network_density_figures(df, network, is_5ghz)


def data_analyze(pcap_f: str, is_5ghz: bool):

    filename = os.path.basename(pcap_f).replace('.pcap', '')   # '2ghz_1m'
    ta_mac = TA_MAC_5 if is_5ghz else TA_MAC_2

    ### Create Data
    df = data_parser(pcap_f, ta_mac, RA_MAC)
    evaluate_throughput_df(df)
    add_rate_gap_to_df(df)
    df.to_csv(f"./data/sniffed-throughput/{filename}.csv", index=False)

    ### Save Data
    df = pd.read_csv(f"./data/sniffed-throughput/{filename}.csv")

    ### Visualize Data
    plot_network_performance_figures(df, filename)
    export_statistics(df, filename)

def speedtest_analyze(pcap_f: str):
    filename = os.path.basename(pcap_f).replace('.pcap', '')   # '2ghz_1m'
    
    df = pd.read_csv(f"./data/sniffed-throughput/{filename}.csv")
    agg_df = evaluate_speedtest_metrics(df)
    agg_df.to_csv(f"./data/sniffed-throughput/agg_{filename}.csv", index=False)

    # ### Visualize Data
    # plot_network_performance_figures(df, filename)
    # export_statistics(df, filename)

def main():
    # data_analyze(THR_2GHZ_1M, False)
    # data_analyze(THR_2GHZ_10M, False)
    # data_analyze(THR_2GHZ_MOVING, False)
    # data_analyze(THR_5GHZ_1M, True)
    # data_analyze(THR_5GHZ_10M, True)
    # data_analyze(THR_5GHZ_MOVING, True)
    
    speedtest_analyze(THR_2GHZ_1M)
    speedtest_analyze(THR_2GHZ_10M)
    speedtest_analyze(THR_2GHZ_MOVING)
    speedtest_analyze(THR_5GHZ_1M)
    speedtest_analyze(THR_5GHZ_10M)
    speedtest_analyze(THR_5GHZ_MOVING)
    # network_density()


if __name__ == "__main__":
    main()
