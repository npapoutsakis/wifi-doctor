"""
Pcap Parsing Tool
"""

import os
import pyshark
from beacon_packet import BeaconPacket
from data_packet import DataPacket
import pandas as pd
from field_mappings import *
from helper import convert_ssid


BEACON_DISP_FILTER = "wlan.fc.type_subtype == 8 && !eapol"

"""Pyshark"""

"""
    Parsing 1.1
    This function parses all pcap files in the provided folder list and extracts beacon data.
    It then converts the extracted beacon data into a pandas DataFrame and saves it to a CSV file.
"""


# TODO: mexri to df kanei to idio to beacon_parser min epanalamvaneis kwdika
def parse_network_beacon_pcaps(pcap_folder, network_name):
    os.makedirs(f"./data/parsed", exist_ok=True)

    # total beacons per network
    total_beacons = []

    for pcap_file in pcap_folder:
        beacon_packets = beacon_pcap_parser(pcap_file)
        total_beacons.extend(beacon_packets)

    # convert to pandas DataFrame and save to CSV
    df = pd.DataFrame(total_beacons)

    df["channel"] = df["channel"].astype("int32")
    df["rssi"] = df["rssi"].astype("int32")

    df.to_csv(f"./data/parsed/{network_name}.csv", index=False)


def beacon_pcap_parser(pcap_file) -> list[BeaconPacket]:
    beacon_packets = []

    beacon_capture = pyshark.FileCapture(
        pcap_file,
        display_filter=BEACON_DISP_FILTER,
        use_json=True,
    )

    beacon_capture.load_packets()
    for packet in beacon_capture._packets:
        radio = packet.wlan_radio  # 802.11 radio
        wlan = packet.wlan  # 802.11 wlan
        mgt = packet["wlan.mgt"]  # 802.11 wireless LAN mgmt

        ### Skip conditionals

        # Some beacon packets send rssi = 0, drop these packets
        rssi = int(radio.signal_dbm)
        if not hasattr(radio, "signal_dbm") or rssi > -30:
            continue

        # Channel selection, if channel != primary channel drop because
        # beacons from non primary channel have weaker rssi
        channel = None
        tag_fields = mgt._all_fields["wlan.tagged.all"]["wlan.tag"]
        for tag in tag_fields:
            if tag["wlan.tag.number"] == "61":
                channel = tag["wlan.ht.info.primarychannel"]
                break

        # If tag didnt have primary channel, use channel
        if channel is None:
            channel = radio.channel
        # if primary channel different than radio channel, drop
        elif channel != radio.channel:
            continue

        beacon_pkt = BeaconPacket()

        # TODO: in some captures, ssid is in hex form ex. "54:53:43" = TUC
        ssid = convert_ssid(
            mgt._all_fields["wlan.tagged.all"]["wlan.tag"][0]["wlan.ssid"]
        )
        beacon_pkt.ssid = ssid
        beacon_pkt.bssid = wlan.bssid
        # beacon_pkt.ta = wlan.ta
        beacon_pkt.phy_type = radio.phy
        beacon_pkt.channel = channel
        beacon_pkt.frequency = radio.frequency
        beacon_pkt.rssi = rssi  # if not wlan.signal_strength
        beacon_pkt.snr = radio.snr if hasattr(radio, "snr") else None
        beacon_pkt.timestamp = mgt.all.timestamp
        beacon_packets.append(beacon_pkt.__dict__)

    # Uncomment if write in file
    # with open("beacon_packets.json", "w") as f:
    #     f.write(str(beacon_packets))
    # To display pretty on terminal: cat beacon_packets.json | jq
    # sudo apt install jq :)

    return beacon_packets


def data_parser(pcap_file, ap_mac, dev_mac):

    data_packets = []
    # TODO: Fix for only downlink throughput
    # Do i need other subtypes?
    DATA_DISP_FILTER = f"(wlan.fc.type_subtype == 0x0020 || wlan.fc.type_subtype == 0x0028) && ((wlan.ta == {ap_mac} && wlan.ra == {dev_mac})) && !eapol"
    # DATA_DISP_FILTER_PREV = f"(wlan.fc.type_subtype == 0x0020 || wlan.fc.type_subtype == 0x0028) && ((wlan.ta == {ap_mac} && wlan.ra == {dev_mac}) || (wlan.ta == {dev_mac} && wlan.ra == {ap_mac})) && wlan.ra == wlan.da && !eapol"
    data_capture = pyshark.FileCapture(
        pcap_file, display_filter=DATA_DISP_FILTER, use_json=True
    )

    rel_time = float(data_capture[0].frame_info.time_relative)

    # Default value if first data packet(s) have no rssi
    prev_rssi = None

    data_capture.load_packets()
    for packet in data_capture._packets:
        frame = packet.frame_info  # frame
        radio = packet.wlan_radio  # 802.11 radio
        wlan = packet.wlan  # 802.11 wlan

        # Skip conditionals
        rssi = radio.signal_dbm if hasattr(radio, "signal_dbm") else prev_rssi
        if rssi is None:
            continue

        data_pkt = DataPacket()

        data_pkt.retry = bool(
            int(wlan._all_fields["wlan.fc_tree"]["wlan.flags_tree"]["wlan.fc.retry"])
        )
        data_pkt.phy = radio.phy
        data_pkt.mcs = radio.mcs_index
        data_pkt.bandwidth = int(radio.bandwidth)
        data_pkt.short_gi = bool(int(radio.short_gi))
        data_pkt.data_rate = radio.data_rate

        # Some dont contain signal_strength
        data_pkt.rssi = rssi
        data_pkt.frequency = radio.frequency
        # data_pkt.rate_gap = idk if here or analyzer
        data_pkt.timestamp = float(frame.time_relative) - rel_time

        data_packets.append(data_pkt)

        prev_rssi = data_pkt.rssi

    df = pd.DataFrame([data_pkt.__dict__ for data_pkt in data_packets])

    df["bandwidth"] = df["bandwidth"].astype(int)
    df["rssi"] = df["rssi"].astype(int)
    df["phy"] = df["phy"].astype(int)
    df["mcs"] = df["mcs"].astype(int)
    df["data_rate"] = df["data_rate"].astype(float)
    # df.to_csv("./data/data_HOW.csv", index=False)

    return df.copy()


# only export the functions
__all__ = ["beacon_pcap_parser", "data_parser", "parse_network_beacon_pcaps"]
