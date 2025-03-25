"""
Pcap Parsing Tool
"""

import pyshark
from beacon_packet import BeaconPacket
import time

from data_packet import DataPacket

PCAP_FILE = "pcaps/HowIWiFi_PCAP.pcap"
BEACON_DISP_FILTER = "wlan.fc.type_subtype == 8 && !eapol"

# Change AP
AP_MAC = "2C:F8:9B:DD:06:A0"
DEV_MAC = "00:20:A6:FC:B0:36"

# TODO: Some packets are sent to broadcast but receiver address is DEV_MAC, should we keep these? probably not
# if not keep them, remove da == ra
DATA_DISP_FILTER = f"(wlan.fc.type_subtype == 0x0020 || wlan.fc.type_subtype == 0x0028) && ((wlan.ta == {AP_MAC} && wlan.ra == {DEV_MAC}) || (wlan.ta == {DEV_MAC} && wlan.ra == {AP_MAC})) && wlan.ra == wlan.da && !eapol"
# 1.2. (wlan.fc.type_subtype == 0x0020 || wlan.fc.type_subtype == 0x0028) && ((wlan.ta == 2C:F8:9B:DD:06:A0 && wlan.ra == 00:20:A6:FC:B0:36) || (wlan.ra == 2C:F8:9B:DD:06:A0 && wlan.ta == 00:20:A6:FC:B0:36)) && !eapol

"""Pyshark"""

# TODO: create two different captures, one for beacone fr(1.1) one for data fr(1.2)


def beacon_parser(pcap_file) -> list[BeaconPacket]:
    beacon_packets = []

    beacon_capture = pyshark.FileCapture(
        pcap_file,
        display_filter=BEACON_DISP_FILTER,
        use_json=True,
    )

    # data_capture = pyshark.FileCapture(
    #     PCAP_FILE, display_filter=DATA_DISP_FILTER, use_json=True
    # )
    for packet in beacon_capture:
        # radiotap = packet.radiotap  # Radiotap header
        radio = packet.wlan_radio  # 802.11 radio
        wlan = packet.wlan  # 802.11 wlan
        mgt = packet["wlan.mgt"]  # 802.11 wireless LAN mgmt

        beacon_pkt = BeaconPacket()

        # :)
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


# beacon_packets = beacon_parser(PCAP_FILE)


def data_parser(pcap_file, disp_filter) -> list[DataPacket]:
    data_packets = []

    data_capture = pyshark.FileCapture(
        pcap_file, display_filter=disp_filter, use_json=True
    )

    for packet in data_capture:
        radiotap = packet.radiotap  # Radiotap header
        radio = packet.wlan_radio  # 802.11 radio
        wlan = packet.wlan  # 802.11 wlan

        data_pkt = DataPacket()

        data_pkt.phy = radio.phy
        data_pkt.mcs = radio.mcs_index
        # very sus line, dk behavior if bandwidth not 20
        data_pkt.bandwidth = 20 if radio.bandwidth == 0 else radio.bandwidth
        data_pkt.short_gi = bool(radio.short_gi)
        data_pkt.data_rate = radio.data_rate

        # Some dont contain signal_strength
        data_pkt.rssi = (
            radio.signal_dbm if hasattr(radio, "signal_dbm") else prev_rssi
        )  # if not wlan.signal_strength
        data_pkt.frequency = radio.frequency
        # data_pkt.rate_gap = idk if here or analyzer
        data_pkt.seq = wlan.seq
        # data_pkt.timestamp = radiotap.timestamp???

        data_packets.append(data_pkt)

        prev_rssi = data_pkt.rssi

    return data_packets


# data_packets = data_parser(PCAP_FILE, DATA_DISP_FILTER)
