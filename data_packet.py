import json


class DataPacket:
    retry: bool | None = None
    phy: str | None = None
    bandwidth: int | None = None
    short_gi: bool | None = None
    data_rate: float | None = None
    mcs: int | None = None
    rssi: int | None = None
    # rate_gap how, maybe not field but evaluated in perf. analyzer
    # rate_gap: float | None = None
    frequency: int | None = None
    timestamp: float | None = None

    def __repr__(self):
        return json.dumps(self.__dict__, separators=(",", ":"))
