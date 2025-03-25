import json


class DataPacket:
    def __init__(
        self,
        phy: str | None = None,
        bandwidth: int | None = None,
        short_gi: bool | None = None,
        data_rate: float | None = None,
        mcs: int | None = None,
        rssi: int | None = None,
        rate_gap: (
            float | None
        ) = None,  # how, maybe not field but evaluated in perf. analyzer
        frequency: int | None = None,
        seq: int | None = None,
        # timestamp: float | None = None,
    ):
        self.phy = phy
        self.mcs = mcs
        self.bandwidth = bandwidth
        self.short_gi = short_gi
        self.data_rate = data_rate
        self.rssi = rssi
        self.rate_gap = rate_gap
        self.frequency = frequency
        self.seq = seq
        # self.timestamp = timestamp

    def __repr__(self):
        return json.dumps(self.__dict__, separators=(",", ":"))
