# WiFi Doctor - Networks 2025

# Group 4: 
#       - Nikolaos Papoutsakis  2019030206
#       - Argyris Christakis    2019030078
#       - Michalis Syrianos     2019030058
#       - Swkratis Siganos      2019030097


# Our main idea is to structure a simple .py file to run the 
# use-cases described in the assignment's description.
import pyshark


# First implement the wifi doctor system, and then run the use-cases.
def wifi_sniffer(interface='enp5s0', packet_count=10):

    capture = pyshark.LiveCapture(interface=interface)
    
    
    for i, packet in enumerate(capture.sniff_continuously(packet_count=int(packet_count))):
        print(f"Packet #{i + 1}: {packet}")
        print("=" * 50)

    print(f"Capture complete. {packet_count} packets captured.")

    return



# The parser function will read the .pcap files and return a dictionary of the data.(or json?)
def parser():

    dict = {
        "SSID": "TUC",
        "BSSID": "00:00:00:00:00:00",
        "Channel": "1",
        "RSSI": "-50",
        "Security": "WPA2",
        "Beacon": "100",   
        }



    return dict






def main():

    # Run the wifi sniffer
    wifi_sniffer()


    return




if __name__ == "__main__":
    main()