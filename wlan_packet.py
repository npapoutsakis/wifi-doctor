import json
from typing import Optional, List, Dict
import random


# Deprecated :)
class wlan_packet:
    def __init__(
        self,
        ssid: str | None = None,
        bssid: str | None = None,
        ta: str | None = None,  # maybe sa?
        ra: str | None = None,
        wlan_type: int | None = None,
        wlan_subtype: int | None = None,
        phy_type: str | None = None,
        mcs_index: int | None = None,
        bandwidth: int | None = None,
        short_gi: bool | None = None,
        data_rate: float | None = None,
        channel: int | None = None,
        frequency: int | None = None,
        rssi: int | None = None,
        timestamp: float | None = None,
        snr: int | None = None,
        spatial_streams: int | None = None,
    ):
        self.ssid = ssid
        self.bssid = bssid
        self.ta = ta
        self.ra = ra
        self.wlan_type = wlan_type
        self.wlan_subtype = wlan_subtype
        self.phy_type = phy_type
        self.mcs_index = mcs_index
        self.bandwidth = bandwidth
        self.short_gi = short_gi
        self.data_rate = data_rate
        self.channel = channel
        self.frequency = frequency
        self.rssi = rssi
        self.timestamp = timestamp
        self.snr = snr
        self.spatial_streams = spatial_streams

    # @classmethod
    # def read_wlan_packet(cls, data: Dict) -> "wlan_packet":
    #     """Create a wlan packet from json deserialization."""
    #     return cls(
    #         ssid=data["ssid"],
    #         bssid=data["bssid"],
    #         transmitter_mac=data["transmitter_mac"],
    #         receiver_mac=data["receiver_mac"],
    #         wlan_type=data["wlan_type"],
    #         wlan_subtype=data["wlan_subtype"],
    #         phy_type=data["phy_type"],
    #         mcs_index=data["mcs_index"],
    #         bandwidth=data["bandwidth"],
    #         short_gi=data["short_gi"],
    #         data_rate=data["data_rate"],
    #         channel=data["channel"],
    #         frequency=data["frequency"],
    #         rssi=data["rssi"],
    #         snr=data["snr"],
    #         spatial_streams=data["spatial_streams"],
    #     )

    def __repr__(self):
        return f"wlan packet(ssid={self.ssid}, signal={self.rssi} dBm)"


# def save_packets_to_json(packet: "wlan_packet", file: str):
#     """Append packet to json file"""
#     with open(file, "a") as f:
#         json.dump(packet, f, indent=2)


# def load_packets_from_json(file: str) -> List[wlan_packet]:
#     """Load packet from a json file."""
#     with open(file, "r") as f:
#         data = json.load(f)
#     return [wlan_packet.from_dict(p) for p in data]


def random_wlan_packet():
    return wlan_packet(
        ssid=f"SSID_{random.randint(1, 100)}",
        bssid=f"{random.randint(0, 255):02x}:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}",
        transmitter_mac=f"{random.randint(0, 255):02x}:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}",
        receiver_mac=f"{random.randint(0, 255):02x}:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}",
        wlan_type=random.randint(0, 255),
        wlan_subtype=random.randint(0, 255),
        phy_type=random.choice(["HT", "VHT", "HE"]),
        mcs_index=random.randint(0, 31),
        bandwidth=random.choice([20, 40, 80, 160]),
        short_gi=random.choice([True, False]),
        data_rate=random.uniform(1.0, 1000.0),
        channel=random.randint(1, 14),
        frequency=random.randint(2412, 2484),
        timestamp=27.0002,
        rssi=random.randint(-100, 0),
        snr=random.randint(0, 40),
        spatial_streams=random.randint(1, 8),
    )


def main():
    # Create 3 random wlan_packet objects
    packets = [random_wlan_packet() for _ in range(3)]
    packets[0].spatial_streams = None

    # Save the packets to a JSON file
    # with open("packets.json", "a") as f:
    #     json.dump([packet.__dict__ for packet in packets], f, indent=2)

    # Load the packets from the JSON file
    # packets = load_packets_from_json("packets.json")

    # Print the packets
    for packet in packets:
        print(packet)


# main()
## test
