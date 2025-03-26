import matplotlib.pyplot as plt
import numpy as np

from data_packet import DataPacket


# TODO: Change all dat, use np, reconsider what is good, poor etc.
def plot_throughput(t, data):
    # t = np.array([pkt.timestamp for pkt in data])
    # thresholds = [0, 25, 75, 150, 250, max(throughput) + 50] # keep???
    plt.plot(t, data)

    plt.tight_layout()
    plt.show()
    return


# # 1. Προσομοίωση δεδομένων για 5 λεπτά (300 δευτερόλεπτα)
# t = np.arange(0, 300, 1)  # χρόνος σε δευτερόλεπτα
# np.random.seed(42)  # για αναπαραγωγιμότητα
# throughput = 50 + 250 * np.sin(2 * np.pi * t / 300) + 50 * np.random.rand(len(t))

# # 2. Ορισμός ορίων για τις κατηγορίες
# thresholds = [0, 25, 75, 150, 250, max(throughput) + 50] # keep???

# # 3. Χρώματα για κάθε ζώνη - πιο έντονα
# colors = [
#     "#ff0000",  # Very Poor (έντονο κόκκινο)
#     "#ff6666",  # Poor (λαμπερό κόκκινο/ροζ)
#     "#ffff66",  # Moderate (έντονο κίτρινο)
#     "#99ff66",  # Good (ανοιχτό πράσινο)
#     "#00ff00",  # Excellent (έντονο πράσινο)
# ]

# # 4. Δημιουργία του plot
# fig, ax = plt.subplots(figsize=(10, 5))

# # Ζωγραφίζουμε οριζόντιες ζώνες (horizontal spans) για κάθε κατηγορία
# for i in range(len(thresholds) - 1):
#     ax.axhspan(thresholds[i], thresholds[i + 1], color=colors[i], alpha=0.3)

# # 5. Σχεδιάζουμε την καμπύλη του throughput
# ax.plot(t, throughput, label="Throughput (Mbps)", color="blue")

# # 6. Ρυθμίσεις του plot
# ax.set_xlabel("Time (seconds)")
# ax.set_ylabel("Throughput (Mbps)")
# ax.set_title("Throughput vs. Time with Performance Bands (Intense Colors)")
# ax.set_xlim([0, 300])  # Για 5 λεπτά
# ax.set_ylim([0, thresholds[-1]])
# ax.legend()

# plt.tight_layout()
# plt.show()
