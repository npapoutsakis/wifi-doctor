import numpy as np
from data_packet import DataPacket


# TODO: add rate gap
def evaluate_throughput(packets: list[DataPacket]):
    throughput_arr = np.empty(len(packets), dtype=float)
    timestamps = np.empty(len(packets), dtype=float)
    retransmits = 0
    for i, packet in enumerate(packets):
        if packet.retry:
            retransmits += 1
        frame_loss_rate = retransmits / (i + 1)
        
        
        timestamps[i] = packet.timestamp
        throughput_arr[i] = float(packet.data_rate) * (1.0 - frame_loss_rate)

    return timestamps, throughput_arr








    # def performance_monitor(
    #     data_rate,
    #     frame_loss_rate,
    #     signal_strength,
    #     snr,
    #     mcs_index,
    #     bandwidth,
    #     spatial_streams,
    #     short_gi,
    # ):

    #     throughput = evaluate_wifi_performance(
    #         data_rate,
    #         frame_loss_rate,
    #         signal_strength,
    #         snr,
    #         bandwidth,
    #         spatial_streams,
    #         short_gi,
    #     )

    #     if throughput > 250:
    #         return "Excellent"
    #     elif throughput > 150:
    #         return "Good"
    #     elif throughput > 75:
    #         return "Moderate"
    #     elif throughput > 25:
    #         return "Poor"
    #     else:
    #         return "Very Poor"

    # def calculate_loss_rate(packets):

    #     total_packets = len(packets)
    #     if total_packets == 0:
    #         return 0.0  # Αν δεν υπάρχουν πακέτα, το loss rate είναι 0

    #     # Υποθέτουμε ότι κάθε packet έχει ένα πεδίο "is_lost" (True/False)
    #     lost_packets = sum(1 for pkt in packets if pkt.get("is_lost", False))

    #     return lost_packets / total_packets

    """
    Υπολογίζει το ποσοστό απώλειας πλαισίων (frame loss rate).
    
    Παράμετροι:
    - packets (list): Μια λίστα με πακέτα ή πλαίσια. Κάθε στοιχείο μπορεί να είναι
      λεξικό ή αντικείμενο που περιέχει μια ένδειξη για το αν το πακέτο χάθηκε.
      
    Επιστρέφει:
    - float: Ένας αριθμός μεταξύ 0 και 1 που εκφράζει το ποσοστό απώλειας.
    """
