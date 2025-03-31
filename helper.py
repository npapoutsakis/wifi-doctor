# Converts a hex SSID into a string
def convert_ssid(hex_ssid: str):
    # Temporary fix
    if hex_ssid.count(":") >= 3:
        hex_str = hex_ssid.replace(":", "")
        bytes_data = bytes.fromhex(hex_str)
        return bytes_data.decode("ascii")
    else:
        return hex_ssid


CHANNELS_5GHZ = columns = [
    36,
    40,
    44,
    48,
    52,
    56,
    60,
    64,
    68,
    100,
    104,
    108,
    112,
    116,
    120,
    124,
    128,
    132,
    136,
    140,
    144,
    149,
    153,
    157,
    161,
    165,
]
