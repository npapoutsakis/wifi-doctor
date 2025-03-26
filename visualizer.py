import matplotlib.pyplot as plt
import numpy as np

t = np.arange(0, 300, 1)  # χρόνος σε δευτερόλεπτα
np.random.seed(42)  # για αναπαραγωγιμότητα
throughput = 50 + 250 * np.sin(2 * np.pi * t / 300) + 50 * np.random.rand(len(t))

# 2. Ορισμός ορίων για τις κατηγορίες
thresholds = [0, 25, 75, 150, 250, max(throughput) + 50]

colors = [
    "#ff0000",  # Very Poor
    "#ff6666",  # Poor
    "#ffff66",  # Moderate
    "#99ff66",  # Good
    "#00ff00",  # Excellent
]

fig, ax = plt.subplots(figsize=(10, 5))

for i in range(len(thresholds) - 1):
    ax.axhspan(thresholds[i], thresholds[i + 1], color=colors[i], alpha=0.3)

ax.plot(t, throughput, label="Throughput (Mbps)", color="blue")

ax.set_xlabel("Time (seconds)")
ax.set_ylabel("Throughput (Mbps)")
ax.set_title("Throughput vs. Time with Performance Bands (Intense Colors)")
ax.set_xlim([0, 300])  # Για 5 λεπτά
ax.set_ylim([0, thresholds[-1]])
ax.legend()

plt.tight_layout()
plt.show()
