import numpy as np
import pandas as pd
from data_packet import DataPacket
from field_mappings import *


# Ref https://wlanprofessionals.com/mcs-table-and-how-to-use-it/
def get_exp_rate_80211n(rssi: int):
    if rssi >= -64:
        return 7
    elif rssi == -65:
        return 6
    elif rssi == -66:
        return 5
    elif rssi >= -70:
        return 4
    elif rssi >= -74:
        return 3
    elif rssi >= -77:
        return 2
    elif rssi >= -82:
        return 1
    else:
        return 0


def rate_gap(df: pd.DataFrame):
    rate_gap_arr = np.empty(df.shape[0], dtype=int)  # get rows

    for index, packet in df.iterrows():
        if phy_type_mapping[packet.get("phy")] == "802.11n":
            gap = rate_gap_80211n(packet.get("rssi"), packet.get("mcs"))
            rate_gap_arr[index] = gap
        else:
            print("Non-802.11n packet")

    return rate_gap_arr


def rate_gap_80211n(rssi: int, rate: int):
    # Check that rssi exists in packet, if not change monitor to always include a value
    assert rssi is not None

    exp_rate = get_exp_rate_80211n(rssi)

    # 1 spatial stream
    if rate < 8:
        gap = exp_rate - rate

    # 2 spatials streams
    elif rate < 16:
        gap = exp_rate + 8 - rate

    # 3 spatials streams
    else:
        gap = exp_rate + 16 - rate

    return gap
