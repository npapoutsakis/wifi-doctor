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
from visualizer import *
from field_mappings import *
import pandas as pd


AP_MAC = "2C:F8:9B:DD:06:A0"
DEV_MAC = "00:20:A6:FC:B0:36"
PCAP_HOW = "./pcaps/HowIWiFi_PCAP.pcap"
PCAP_FILE_5GHZ = "./beacon_pcaps/tuc-5ghz/52_80.pcap"

PCAP_FILES_5GHZ_TUC = [
    "./beacon_pcaps/esties-5ghz/channel_36.pcap",
    "./beacon_pcaps/esties-5ghz/channel_40.pcap",
    "./beacon_pcaps/esties-5ghz/channel_44.pcap",
    "./beacon_pcaps/esties-5ghz/channel_48.pcap",
]

PCAP_FILES_2_4_GHZ_TUC = [
    "./beacon_pcaps/esties-2.4ghz/channel_1.pcap",
    "./beacon_pcaps/esties-2.4ghz/channel_2.pcap",
    "./beacon_pcaps/esties-2.4ghz/channel_3.pcap",
    "./beacon_pcaps/esties-2.4ghz/channel_4.pcap",
    "./beacon_pcaps/esties-2.4ghz/channel_5.pcap",
    "./beacon_pcaps/esties-2.4ghz/channel_6.pcap",
    "./beacon_pcaps/esties-2.4ghz/channel_7.pcap",
    "./beacon_pcaps/esties-2.4ghz/channel_8.pcap",
    "./beacon_pcaps/esties-2.4ghz/channel_9.pcap",
    "./beacon_pcaps/esties-2.4ghz/channel_10.pcap",
    "./beacon_pcaps/esties-2.4ghz/channel_11.pcap",
    "./beacon_pcaps/esties-2.4ghz/channel_12.pcap",
    "./beacon_pcaps/esties-2.4ghz/channel_13.pcap",
]


##################################################################################################################
"""
    Scenario 1.1: WiFi Network Density
"""


# Converts a hex SSID into a string
def convert_ssid(hex_ssid):
    hex_str = hex_ssid.replace(":", "")
    bytes_data = bytes.fromhex(hex_str)
    return bytes_data.decode("ascii")


def performance_monitor():

    # make a large dataset of all channels of 2.4GHz (TUC) and save them on a .csv file
    total_beacons = []
    for pcap_file in PCAP_FILES_2_4_GHZ_TUC:
        beacon_packets = beacon_parser(pcap_file)
        for beacon in beacon_packets:
            total_beacons.append(
                {
                    "SSID": convert_ssid(beacon.ssid),
                    "BSSID": beacon.bssid,
                    "PHY": phy_type_mapping.get(beacon.phy_type),
                    "CHANNEL": beacon.channel,
                    "FREQUENCY": beacon.frequency,
                    "RSSI(dBm)": beacon.rssi,
                    "SNR(dB)": beacon.snr,
                }
            )

    # this should be on parser side
    df = pd.DataFrame(total_beacons)

    # Convert columns to appropriate data types
    df["CHANNEL"] = df["CHANNEL"].astype("int32")
    df["RSSI(dBm)"] = df["RSSI(dBm)"].astype("int32")

    # Save to csv file
    # df.to_csv("./data/tuc_2_4ghz_beacons.csv", index=True)

    plot_rssi_vs_frequency(df)
    plot_channel_occupancy_by_ssid(df)


def data_analyze():
    packets = data_parser(PCAP_HOW, AP_MAC, DEV_MAC)
    t, throughput_arr = evaluate_throughput(packets)
    print(np.min(throughput_arr))
    print(np.max(throughput_arr))
    print(np.mean(throughput_arr))
    plot_throughput(t, throughput_arr)


def main():
    data_analyze()


if __name__ == "__main__":
    main()
