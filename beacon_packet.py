import json


class BeaconPacket:
    ssid: str | None = None
    bssid: str | None = None
    # ta: str | None = None
    phy_type: str | None = None
    channel: int | None = None
    frequency: int | None = None
    rssi: float | None = None
    snr: float | None = None
    timestamp: float | None = None

    def __repr__(self):
        return json.dumps(self.__dict__, separators=(",", ":"))
