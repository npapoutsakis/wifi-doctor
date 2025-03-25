import json


class BeaconPacket:
    def __init__(
        self,
        ssid: str | None = None,
        bssid: str | None = None,
        ta: str | None = None,
        phy_type: str | None = None,
        channel: int | None = None,
        frequency: int | None = None,
        rssi: float | None = None,
        snr: float | None = None,
        timestamp: float | None = None,
    ):
        self.ssid = ssid
        self.bssid = bssid
        self.ta = ta
        self.phy_type = phy_type
        self.channel = channel
        self.frequency = frequency
        self.rssi = rssi
        self.snr = snr
        self.timestamp = timestamp

    def __repr__(self):
        return json.dumps(self.__dict__, separators=(",", ":"))
