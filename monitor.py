import numpy as np
from data_packet import DataPacket
import pandas as pd
from field_mappings import *
from pcap_parser import *


# TODO: add rate gap
def evaluate_throughput(packets: list[DataPacket]):
    throughput_arr = np.empty(len(packets), dtype=float)
    timestamps = np.empty(len(packets), dtype=float)
    retransmits = 0
    for i, packet in enumerate(packets):
        if packet.retry:
            retransmits += 1
        frame_loss_rate = retransmits / (i + 1)

        timestamps[i] = packet.timestamp
        throughput_arr[i] = float(packet.data_rate) * (1.0 - frame_loss_rate)

    return timestamps, throughput_arr


def calculate_network_density():

    # TODO: implement this function
    # rssid metric: Pefkianakis et al. “Characterizing Home Wireless Performance: The Gateway View”, IEEE INFOCOM 2015
    # rssid = Sum(1/rssi)

    return


def monitor_1_1():
    # TODO: implement this function
    return
