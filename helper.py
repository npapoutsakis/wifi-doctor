# Converts a hex SSID into a string
def convert_ssid(hex_ssid: str):
    # Temporary fix
    if hex_ssid.count(":") >= 3:
        hex_str = hex_ssid.replace(":", "")
        bytes_data = bytes.fromhex(hex_str)
        return bytes_data.decode("ascii")
    else:
        return hex_ssid
