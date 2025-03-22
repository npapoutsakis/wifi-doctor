"""
    WiFi Sniffing Tool  (Debian/Ubuntu)

    It will monitor the packets transmitted over Wi-Fi. You will use Wireshark to monitor the Wi-Fi 
    network as you learned in lab 1. The output of the Wi-Fi Sniffer will be a .pcap file

"""

import pyshark
import subprocess
import os
import logging
import time


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
"""
def sniffing():
    try:
        logging.info(f"Starting packet sniffing on mon0 . . .")
        capture = pyshark.LiveCapture(interface="mon0", output_file = "sniffed_packets.pcap")
        for packet in capture.sniff_continuously(packet_count=100):
            print(packet)

    except pyshark.TSharkNotFoundException:
        logging.error("TShark not found. Please install it.")
        exit(-1)
    except PermissionError:
        logging.error("Permission denied. Run the script with sudo.")
        exit(-1)
    except Exception as e:
        logging.error(f"An error occurred during sniffing: {e}")
        exit(-1)



"""
    Future Work:
    - add the ability to use macos environment
    - add the ability to change the mode of the already extisting wifi interface and then restart the network service
    - add the ability to save the .pcap file on the project directory -> DONE

"""

# Running sniffer.py
if __name__ == "__main__":

    # Enable Monitor Mode
    # Enable Packet Sniffing
    # Capture Packets
    # Disable Monitor Mode
    # Save the .pcap file on the project directory

    monitor_mode()
    # time.sleep(2)
    # sniffing()
    capture = pyshark.LiveCapture(interface="mon0")
    # for packet in capture.sniff_continuously():
    #     print(packet)
    capture.sniff(timeout=10)
    disable_monitor_mode()
    logging.info("Packets sniffed successfully")
    logging.info("Exiting . . .")
    exit(0)
