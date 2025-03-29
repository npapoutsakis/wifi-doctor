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

    def to_dict(self):
        return {
            "SSID": self.ssid,
            "BSSID": self.bssid,
            # "TA": self.ta,
            "PHY": self.phy_type,
            "CHANNEL": self.channel,
            "FREQUENCY": self.frequency,
            "RSSI(dBm)": self.rssi,
            "SNR(dB)": self.snr,
            "TIMESTAMP": self.timestamp,
        }
