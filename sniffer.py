"""
    WiFi Sniffing Tool  (Debian/Ubuntu)

    It will monitor the packets transmitted over Wi-Fi. You will use Wireshark to monitor the Wi-Fi 
    network as you learned in lab 1. The output of the Wi-Fi Sniffer will be a .pcap file

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
"""
def sniffing(pcap_file='sniffed.pcap',packet_count=1000):
    logging.info(f"Starting packet sniffing on mon0 . . .")

    """
        subprocess.run command here cannot directly write the output to a file
        so, we have to use f.open().
    """
    f = open(pcap_file, "w")
    subprocess.run(["sudo", "tshark", "-i", "mon0", '-c', str(packet_count), '-w', pcap_file], check=True, capture_output=False)

    f.close()
    logging.info(f"Pcap saved . . .")
    
    return



"""
    Future Work:
    - add the ability to use macos environment - OPTIONAL
    - add the ability to change the mode of the already extisting wifi interface and then restart the network service - NOT NEEDED
    - add the ability to save the .pcap file on the project directory -> DONE

"""

# Running sniffer.py
if __name__ == "__main__":
    monitor_mode()
    sniffing()
    disable_monitor_mode()
    logging.info("Sniffering exited successfully . . .")
    exit(0)
