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

from parser import *
from monitor import evaluate_throughput
import numpy as np

# from visualizer import *

AP_MAC = "2C:F8:9B:DD:06:A0"
DEV_MAC = "00:20:A6:FC:B0:36"
PCAP_FILE = "pcaps/HowIWiFi_PCAP.pcap"


def main():
    packets = data_parser(PCAP_FILE, AP_MAC, DEV_MAC)
    throughput_arr = evaluate_throughput(packets)
    print(np.min(throughput_arr))
    print(np.max(throughput_arr))
    print(np.mean(throughput_arr))
    # plot_throughput(throughput_arr, "Throughput")
    return


if __name__ == "__main__":
    main()
