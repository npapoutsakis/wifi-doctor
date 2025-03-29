import numpy as np
from data_packet import DataPacket
from rate_gap import rate_gap


def analyze_packets(packets: list[DataPacket]):
    packet = packets[0]
    packet.mcs
    phy_list = np.vectorize(lambda pkt: pkt.phy)(packets)
    short_gi_list = np.vectorize(lambda pkt: pkt.short_gi)(packets)
    phy_list = np.vectorize(lambda pkt: pkt.mcs)(packets)
    # Fix for other protocols
    phy_list = np.vectorize(lambda pkt: rate_gap(pkt))(packets)
    bandwidth_list = np.vectorize(lambda pkt: pkt.bandwidth)(packets)
    rssi_list = np.vectorize(lambda pkt: pkt.rssi)(packets)

    return
