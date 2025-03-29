from data_packet import DataPacket


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


def rate_gap_80211n(packet: DataPacket):
    rssi = packet.rssi

    # Check that rssi exists in packet, if not change monitor to always include a value
    assert rssi is not None

    rate = packet.mcs
    exp_rate = get_exp_rate_80211n(packet.rssi)

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
