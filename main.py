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

from analyzer import analyze_data_packets
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


# pcap files sniffed
PCAP_FILES_2_4_GHZ_HOME = glob.glob("./beacon_pcaps/home-2.4ghz/*.pcap")
PCAP_FILES_2_4_GHZ_TUC = glob.glob("./beacon_pcaps/tuc-2.4ghz/*.pcap")
PCAP_FILES_5_GHZ_HOME = glob.glob("./beacon_pcaps/home-5ghz/*.pcap")
PCAP_FILES_5_GHZ_TUC = glob.glob("./beacon_pcaps/tuc-5ghz/*.pcap")


"""
    Scenario 1.1: WiFi Network Density
"""


def network_density():

    pcap_folder_list_2_4_ghz = [PCAP_FILES_2_4_GHZ_TUC, PCAP_FILES_2_4_GHZ_HOME]
    # pcap_folder_list_5_ghz = [PCAP_FILES_5_GHZ_TUC, PCAP_FILES_5_GHZ_HOME]

    # Parsing -> saves v files
    parse_beacon_folders(pcap_folder_list_2_4_ghz)
    # parse_beacon_folders(pcap_folder_list_5_ghz)

    # monitor and calculate network density
    network_files = {
        "TUC-2.4GHz": "./data/tuc-2.4ghz.csv",
        # "TUC-5GHz": "./data/tuc-5ghz.csv",
        "HOME-2.4GHz": "./data/home-2.4ghz.csv",
        # "HOME-5GHz":"./data/home-5ghz.csv",
    }

    # # monitor each network file
    monitor_1_1(network_files)

    # visualize
    df = pd.read_csv(network_files["HOME-2.4GHz"])
    plot_rssi_vs_frequency(df)

    # return


def data_analyze():

    data_parser(PCAP_HOW, AP_MAC, DEV_MAC)

    # read multiple csv's?
    df = pd.read_csv("./data/data_HOW.csv")

    # t1, throughput_arr1 = evaluate_throughput_list(packets)
    throughput_arr = evaluate_throughput_df(df)

    # print(np.min(throughput_arr))
    # print(np.max(throughput_arr))
    # print(np.mean(throughput_arr))

    rate_gap_arr = analyze_data_packets(df)

    plot_rate_gap(df["timestamp"], rate_gap_arr)
    # plot_throughput(t1, throughput_arr1)
    # plot_throughput_df(df2)

    plt.show()


def main():
    data_analyze()
    # Uncomment gia to diko sou
    # network_density()


if __name__ == "__main__":
    main()
