"""
    WiFi Sniffing Tool  (Debian/Ubuntu)

    It will monitor the packets transmitted over Wi-Fi. You will use Wireshark to monitor the Wi-Fi 
    network as you learned in lab 1. The output of the Wi-Fi Sniffer will be a .pcap file

    Run:
        sudo python3 sniffer.py

"""

import subprocess
import os
import logging

# import pyshark -- garbage, not working maybe use scapy, or tshark
# https://github.com/KimiNewt/pyshark/issues/92


"""
    Logging Configuration
"""
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s]: %(message)s"
)


"""
    Enabling Monitor Mode
"""
def monitor_mode():

    # ask for root privileges
    if os.geteuid() != 0:
        logging.error("This script requires root privileges. Please run with sudo.")
        exit(-1)

    # get the wireless interface
    interface = ""

    result = subprocess.run(["iw", "dev"], capture_output=True, text=True, check=True)
    for line in result.stdout.split("\n"):
        if "Interface" in line:
            interface = line.split(" ")[1]
            break
    
    if interface == "":
        logging.error("No wireless interface found")
        exit(-1)


    logging.info(f"Wireless interface found: {interface}")
    
    # Check if the interface is already in monitor mode
    result = subprocess.run(["iw", interface, "info"], capture_output=True, text=True, check=True)
    if "monitor" in result.stdout:
        logging.info("Interface is already in monitor mode")
        return


    # Create a new interface in monitor mode (lab 1 commands)
    logging.info(f"Creating a new interface in monitor mode from {interface}")

    subprocess.run(["iw", "dev", interface, "interface", "add", "mon0", "type", "monitor"], check=True)
    logging.info(f"Interface mon0 created from {interface}")


    # Start the interface
    subprocess.run(["ifconfig", "mon0", "up"], check=True)
    logging.info("Interface mon0 is up")

    return



"""
    Disabling Monitor Mode 
"""
def disable_monitor_mode():
    # ask for root privileges
    if os.geteuid() != 0:
        logging.error("This script requires root privileges. Please run with sudo.")
        exit(-1)

    # delete the interface
    logging.info("Deleting interface mon0")
    subprocess.run(["iw", "dev", "mon0", "del"], check=True)
    logging.info("Interface mon0 deleted")

    # verifying
    result = subprocess.run(["iw", "dev"], capture_output=True, text=True, check=True)
    for line in result.stdout.split("\n"):
        if "mon0" in line:
            logging.error("Interface mon0 still exists")
            exit(-1)

    return



"""
    Sniffing Packets and saves them in a .pcap file
    tshark [ -i <capture interface>|- ] [ -f <capture filter> ] [ -2 ] [ -r <infile> ] [ -w <outfile>|- ] [ options ] [ <filter> ] [-c number of packets]
    When timeout is 0, it will sniff for packet_count packets
"""
def sniffing(pcap_file, timeout = 0, packet_count = 500):
    logging.info(f"Starting packet sniffing on mon0 . . .")

    """
        subprocess.run command here cannot directly write the output to a file
        so, we have to use f.open().
    """
    f = open(pcap_file, "w")
    if timeout:
        # with timeout
        subprocess.run(["sudo", "tshark", "-i", "mon0", '-w', pcap_file, '-a', f"duration:{timeout}"], check=True, capture_output=False)
    else:
        subprocess.run(["sudo", "tshark", "-i", "mon0", '-c', str(packet_count), '-w', pcap_file], check=True, capture_output=False)

    f.close()
    logging.info(f"Pcap saved . . .")
    return


"""
    Sniffing Packets on all channels
"""
def sniff_from_all_channels():

    logging.info(f"Starting packet sniffing on all channels . . .")

    for channel in range(1, 14): #(2.4GHz)
        logging.info(f"Sniffing channel {channel} . . .")

        # disable the interface
        # subprocess.run(["sudo", "ifconfig", "mon0", "down"], check=True, capture_output=False)

        # set the channel
        subprocess.run(["sudo", "iw", "dev", "mon0", "set", "channel", str(channel)], check=True, capture_output=False)
        
        sniffing(f"sniff_all/channel_{channel}.pcap", timeout=10)

        # maybe use mergecap to merge all the pcap files
        # but the timing of the packets will be lost
        # subprocess.run(["mergecap", "-w", "sniff_all.pcap", "sniff_all/*.pcap"], check=True, capture_output=False)
        logging.info(f"Pcap saved . . .")

    return


# Running sniffer.py
if __name__ == "__main__":
    monitor_mode()
    sniffing("pcaps/sniff.pcap")
    # sniff_from_all_channels()
    disable_monitor_mode()
    logging.info("Sniffering exited successfully . . .")
    exit(0)
