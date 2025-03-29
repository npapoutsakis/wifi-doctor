# Converts a hex SSID into a string
def convert_ssid(hex_ssid):
    hex_str = hex_ssid.replace(":", "")
    bytes_data = bytes.fromhex(hex_str)
    return bytes_data.decode("ascii")
