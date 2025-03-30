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


def data_analyze(network: str):

    ### Create Data
    df = data_parser(PCAP_HOW, AP_MAC, DEV_MAC)
    evaluate_throughput_df(df)
    add_rate_gap_to_df(df)
    df.to_csv("./data/how.csv", index=False)

    ### Save Data?

    ### Visualize Data
    # read multiple csv's?

    # print(np.min(throughput_arr))
    # print(np.max(throughput_arr))
    # print(np.mean(throughput_arr))

    # plot rssi vs phytype an allazei
    # plot rssi vs rategap gia megali apostasi
    # plot bandwidth vs rssi? gia 5ghz >bandwidth, isos otan peftei rssi peftei bandiwdth?
    plot_network_performance_figures(df, network)
    # print((df["short_gi"].values == False).sum())
    # print((df["short_gi"].values == True).sum())
    export_statistics(df, network)


def main():
    data_analyze("HOW")
    # Uncomment gia to diko sou
    # network_density()


if __name__ == "__main__":
    main()
