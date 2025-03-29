"""
Pcap Parsing Tool
"""

import pyshark
from beacon_packet import BeaconPacket
import time
from data_packet import DataPacket

BEACON_DISP_FILTER = "wlan.fc.type_subtype == 8 && !eapol"

"""Pyshark"""


def beacon_parser(pcap_file) -> list[BeaconPacket]:
    beacon_packets = []

    beacon_capture = pyshark.FileCapture(
        pcap_file,
        display_filter=BEACON_DISP_FILTER,
        use_json=True,
    )

    beacon_capture.load_packets()
    for packet in beacon_capture._packets:
        # radiotap = packet.radiotap  # Radiotap header
        radio = packet.wlan_radio  # 802.11 radio
        wlan = packet.wlan  # 802.11 wlan
        mgt = packet["wlan.mgt"]  # 802.11 wireless LAN mgmt

        beacon_pkt = BeaconPacket()

        # TODO: in some captures, ssid is in hex form ex. "54:53:43" = TUC
        beacon_pkt.ssid = mgt._all_fields["wlan.tagged.all"]["wlan.tag"][0]["wlan.ssid"]
        beacon_pkt.bssid = wlan.bssid
        beacon_pkt.ta = wlan.ta
        beacon_pkt.phy_type = radio.phy
        beacon_pkt.channel = radio.channel
        beacon_pkt.frequency = radio.frequency
        beacon_pkt.rssi = radio.signal_dbm  # if not wlan.signal_strength
        beacon_pkt.snr = radio.snr if hasattr(radio, "snr") else None
        beacon_pkt.timestamp = mgt.all.timestamp
        beacon_packets.append(beacon_pkt)

    # Uncomment if write in file
    # with open("beacon_packets.json", "w") as f:
    #     f.write(str(beacon_packets))
    # To display pretty on terminal: cat beacon_packets.json | jq
    # sudo apt install jq :)

    return beacon_packets


def data_parser(pcap_file, ap_mac, dev_mac) -> list[DataPacket]:

    data_packets = []
    # TODO: Fix for only downlink throughput
    # Do i need other subtypes?
    DATA_DISP_FILTER = f"(wlan.fc.type_subtype == 0x0020 || wlan.fc.type_subtype == 0x0028) && ((wlan.ta == {ap_mac} && wlan.ra == {dev_mac})) && !eapol"
    # DATA_DISP_FILTER_PREV = f"(wlan.fc.type_subtype == 0x0020 || wlan.fc.type_subtype == 0x0028) && ((wlan.ta == {ap_mac} && wlan.ra == {dev_mac}) || (wlan.ta == {dev_mac} && wlan.ra == {ap_mac})) && wlan.ra == wlan.da && !eapol"
    data_capture = pyshark.FileCapture(
        pcap_file, display_filter=DATA_DISP_FILTER, use_json=True
    )

    rel_time = float(data_capture[0].frame_info.time_relative)
    prev_rssi = None

    data_capture.load_packets()
    for packet in data_capture._packets:
        frame = packet.frame_info  # frame
        radio = packet.wlan_radio  # 802.11 radio
        wlan = packet.wlan  # 802.11 wlan

        data_pkt = DataPacket()

        data_pkt.retry = bool(
            int(wlan._all_fields["wlan.fc_tree"]["wlan.flags_tree"]["wlan.fc.retry"])
        )
        data_pkt.phy = radio.phy
        data_pkt.mcs = radio.mcs_index
        data_pkt.bandwidth = radio.bandwidth
        data_pkt.short_gi = bool(radio.short_gi)
        data_pkt.data_rate = radio.data_rate

        # Some dont contain signal_strength
        data_pkt.rssi = (
            radio.signal_dbm if hasattr(radio, "signal_dbm") else prev_rssi
        )  # if not wlan.signal_strength
        data_pkt.frequency = radio.frequency
        # data_pkt.rate_gap = idk if here or analyzer
        data_pkt.timestamp = float(frame.time_relative) - rel_time

        data_packets.append(data_pkt)

        prev_rssi = data_pkt.rssi

    return data_packets


# only export the functions
__all__ = ["beacon_parser", "data_parser"]
