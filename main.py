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
<<<<<<< HEAD

import numpy as np
import glob # used for file globbing :) [*.pcap]
from pcap_parser import *
from monitor import *
from visualizer import *
<<<<<<< HEAD
=======
from field_mappings import *
import pandas as pd

>>>>>>> analyzer
=======

import numpy as np
import glob  # used for file globbing :) [*.pcap]
from pcap_parser import *
from monitor import *
from visualizer import *
>>>>>>> d330f34 (1.1 70% done)

AP_MAC = "2C:F8:9B:DD:06:A0"
DEV_MAC = "00:20:A6:FC:B0:36"
PCAP_HOW = "./pcaps/HowIWiFi_PCAP.pcap"


# pcap files sniffed
PCAP_FILES_2_4_GHZ_HOME = glob.glob("./beacon_pcaps/home-2.4ghz/*.pcap")
PCAP_FILES_2_4_GHZ_TUC = glob.glob("./beacon_pcaps/tuc-2.4ghz/*.pcap")
PCAP_FILES_5_GHZ_HOME = glob.glob("./beacon_pcaps/home-5ghz/*.pcap")
PCAP_FILES_5_GHZ_TUC = glob.glob("./beacon_pcaps/tuc-5ghz/*.pcap")

<<<<<<< HEAD
<<<<<<< HEAD
def data_analyze():
    packets = data_parser(PCAP_HOW, AP_MAC, DEV_MAC)
    t, throughput_arr = evaluate_throughput(packets)
    print(np.min(throughput_arr))
    print(np.max(throughput_arr))
    print(np.mean(throughput_arr))
    plot_throughput(t, throughput_arr)

=======
##################################################################################################################
>>>>>>> analyzer
=======

>>>>>>> d330f34 (1.1 70% done)
"""
    Scenario 1.1: WiFi Network Density
"""
def scenario_1_1():

<<<<<<< HEAD
    # List of pcap files for both 2.4GHz and 5GHz bands
    # pcap_folder_list_2_4_ghz = [PCAP_FILES_2_4_GHZ_TUC, PCAP_FILES_2_4_GHZ_HOME]
    # pcap_folder_list_5_ghz = [PCAP_FILES_5_GHZ_TUC, PCAP_FILES_5_GHZ_HOME]

    # Parsing 1.1
    # parsing_1_1(pcap_folder_list_2_4_ghz)

    # Monitor 1.1 -> will load the csv's and will calculate the network density
    # monitor_1_1()


    # Visualize 1.1


    return    



if __name__ ==  "__main__":
    scenario_1_1()
=======

def scenario_1_1():
    return

    # List of pcap files for both 2.4GHz and 5GHz bands
    # pcap_folder_list_2_4_ghz = [PCAP_FILES_2_4_GHZ_TUC, PCAP_FILES_2_4_GHZ_HOME]
    # pcap_folder_list_5_ghz = [PCAP_FILES_5_GHZ_TUC, PCAP_FILES_5_GHZ_HOME]

    # Parsing 1.1
    # parsing_1_1(pcap_folder_list_2_4_ghz)


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
>>>>>>> analyzer
