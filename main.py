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

from field_mappings import *
import pandas as pd
import numpy as np
import glob  # used for file globbing :) [*.pcap]
from pcap_parser import *
from monitor import *
from visualizer import *


AP_MAC = "2C:F8:9B:DD:06:A0"
DEV_MAC = "00:20:A6:FC:B0:36"
PCAP_HOW = "./pcaps/HowIWiFi_PCAP.pcap"


# pcap files sniffed
PCAP_FILES_2_4_GHZ_HOME = glob.glob("./beacon_pcaps/home-2.4ghz/*.pcap")
PCAP_FILES_2_4_GHZ_TUC = glob.glob("./beacon_pcaps/tuc-2.4ghz/*.pcap")
PCAP_FILES_5_GHZ_HOME = glob.glob("./beacon_pcaps/home-5ghz/*.pcap")
PCAP_FILES_5_GHZ_TUC = glob.glob("./beacon_pcaps/tuc-5ghz/*.pcap")


def data_analyze():
    packets = data_parser(PCAP_HOW, AP_MAC, DEV_MAC)
    t, throughput_arr = evaluate_throughput(packets)
    print(np.min(throughput_arr))
    print(np.max(throughput_arr))
    print(np.mean(throughput_arr))
    plot_throughput(t, throughput_arr)


"""
    Scenario 1.1: WiFi Network Density
"""


def scenario_1_1():
    return


def data_analyze():
    packets = data_parser(PCAP_HOW, AP_MAC, DEV_MAC)
    t, throughput_arr = evaluate_throughput(packets)
    print(np.min(throughput_arr))
    print(np.max(throughput_arr))
    print(np.mean(throughput_arr))
    plot_throughput(t, throughput_arr)


def main():
    data_analyze()
    # Uncomment gia to diko sou
    # scenario_1_1()


if __name__ == "__main__":
    main()
