"""
Pcap Parsing Tool
"""

from scapy.utils import rdpcap
import pyshark
import scapy.layers.dot11 as dot11
import wlan_packet
import json
import time

PCAP_FILE = "pcaps/HowIWiFi_PCAP.pcap"

"""Pyshark"""


# TODO: create two different captures, one for beacone fr(1.1) one for data fr(1.2)
start_time = time.time()
capture = pyshark.FileCapture(PCAP_FILE, use_json=True)
for packet in capture:
    radiotap = packet.radiotap  # Radiotap header
    radio = packet.wlan_radio  # 802.11 radio
    wlan = packet.wlan  # 802.11 wlan


end_time = time.time()
print(f"Time taken: {end_time - start_time} seconds")

# packets = rdpcap(PCAP_FILE, count=1)
# for packet in packets:
#     print(packet)

# wlan_packets = []
# for packet in packets:
#     if packet.haslayer(dot11.Dot11):
#         ssid = packet.info.decode() if packet.haslayer(dot11.Dot11Beacon) else "Unknown"
#         bssid = packet.addr2 if packet.addr2 else "00:00:00:00:00:00"
#         transmitter_mac = packet.addr2 if packet.addr2 else "00:00:00:00:00:00"
#         receiver_mac = packet.addr1 if packet.addr1 else "00:00:00:00:00:00"
#         wlan_type = packet.type if hasattr(packet, "type") else 0
#         wlan_subtype = packet.subtype if hasattr(packet, "subtype") else 0
#         phy_type = "Unknown"
#         mcs_index = 0
#         bandwidth = 20
#         short_gi = False
#         data_rate = 0.0
#         channel = 0
#         frequency = 0
#         rssi = packet.dBm_AntSignal if hasattr(packet, "dBm_AntSignal") else -100
#         timestamp = packet.time if hasattr(packet, "time") else 0.0
#         snr = None
#         spatial_streams = None

#         wlan_packet_obj = wlan_packet(
#             ssid=ssid,
#             bssid=bssid,
#             transmitter_mac=transmitter_mac,
#             receiver_mac=receiver_mac,
#             wlan_type=wlan_type,
#             wlan_subtype=wlan_subtype,
#             phy_type=phy_type,
#             mcs_index=mcs_index,
#             bandwidth=bandwidth,
#             short_gi=short_gi,
#             data_rate=data_rate,
#             channel=channel,
#             frequency=frequency,
#             rssi=rssi,
#             timestamp=timestamp,
#             snr=snr,
#             spatial_streams=spatial_streams,
#         )
#         wlan_packets.append(wlan_packet_obj)


beacon = association_req = association_res = auth = deauth = total = total_wlan = 0


# def save_packets_to_json(packet: "wlan_packet", file: str):
#     """Append packet to json file"""
#     with open(file, "a") as f:
#         json.dump(packet, f, indent=2)


# def get_layers(packet):
#     layers = []
#     while packet:
#         layer = packet.__class__.__name__
#         layers.append(layer)
#         packet = packet.payload
#     return layers


# 1.2. (wlan.fc.type_subtype == 0x0020 || wlan.fc.type_subtype == 0x0028) && wlan.addr == 2C:F8:9B:DD:06:A0 && wlan.addr == 00:20:A6:FC:B0:36


# for packet in packets:
#     if not packet.haslayer(dot11.Dot11Beacon):
#         layers = get_layers(packet)
#         print(layers)
# for packet in packets:
#     total += 1
#     layers = get_layers(packet)
#     if packet.haslayer(dot11.Dot11):
#         total_wlan += 1
#         if packet.haslayer(dot11.Dot11Beacon):
#             beacon += 1
#         elif packet.haslayer(dot11.Dot11AssoReq):
#             association_req += 1
#         elif packet.haslayer(dot11.Dot11AssoResp):
#             association_res += 1
#         elif packet.haslayer(dot11.Dot11Auth):
#             auth += 1
#         elif packet.haslayer(dot11.Dot11Deauth):
#             deauth += 1
# print(f"Total: {total}")
# print(f"Total WLAN: {total_wlan}")
# print(f"Beacon: {beacon}")
# print(f"Association Request: {association_req}")
# print(f"Association Response: {association_res}")
# print(f"Authentication: {auth}")
# print(f"Deauthentication: {deauth}")
