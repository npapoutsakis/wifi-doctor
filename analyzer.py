import numpy as np
import pandas as pd
from data_packet import DataPacket
from rate_gap import rate_gap


def analyze_data_packets(df: pd.DataFrame):

    rate_gap_arr = rate_gap(df)

    # phy_list = np.vectorize(lambda pkt: pkt.phy)(packets)
    # short_gi_list = np.vectorize(lambda pkt: pkt.short_gi)(packets)
    # phy_list = np.vectorize(lambda pkt: pkt.mcs)(packets)
    # Fix for other protocols
    # rate_gap = np.vectorize(lambda pkt: rate_gap(pkt))(packets)
    # bandwidth_list = np.vectorize(lambda pkt: pkt.bandwidth)(packets)
    # rssi_list = np.vectorize(lambda pkt: pkt.rssi)(packets)

    return rate_gap_arr
