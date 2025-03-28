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

from pcap_parser import *
from monitor import evaluate_throughput
import numpy as np
from visualizer import plot_throughput

# from visualizer import *

AP_MAC = "2C:F8:9B:DD:06:A0"
DEV_MAC = "00:20:A6:FC:B0:36"
PCAP_HOW = "./pcaps/HowIWiFi_PCAP.pcap"
PCAP_FILE_5GHZ = "./beacon_pcaps/tuc-5ghz/52_80.pcap"
PCAP_FILE_2GHZ_1 = "./beacon_pcaps/esties-2.4ghz/channel_1.pcap"
PCAP_FILE_2GHZ_2 = "./beacon_pcaps/esties-2.4ghz/channel_2.pcap"

def data_analyze():
    packets = data_parser(PCAP_HOW, AP_MAC, DEV_MAC)
    t, throughput_arr = evaluate_throughput(packets)
    print(np.min(throughput_arr))
    print(np.max(throughput_arr))
    print(np.mean(throughput_arr))
    plot_throughput(t, throughput_arr)
    
def beacon_analyze():
    beacon_packets1 = beacon_parser(PCAP_FILE_2GHZ_1)
    beacon_packets2 = beacon_parser(PCAP_FILE_2GHZ_2)
    beacon_packets3 = beacon_parser(PCAP_FILE_5GHZ)
    print(beacon_packets2)

def main():
    beacon_analyze()


if __name__ == "__main__":
    main()
