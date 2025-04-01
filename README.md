
# WiFi Doctor

A tool for diagnosing Wi-Fi performance issues through passive monitoring, packet parsing, and performance analysis.  
Designed for **Computer Networks II - Spring 2025**.

---

## Project Purpose

WiFi Doctor is designed to passively diagnose Wi-Fi network performance from a device’s perspective. It collects `.pcap` traces, parses relevant fields, monitors throughput and signal metrics, and analyzes bottlenecks. It includes visualizations and exports detailed statistics for both network density and downlink throughput.


---

## Core Features & Function Details

### 1. **WiFi Sniffer** (`sniffer.py`)
- **monitor_mode()**  
  Detects the primary wireless interface, checks if it is in monitor mode, and if not, creates a new monitor mode interface (`mon0`).


- **sniffing(pcap_file, timeout, packet_count)**  
  Invokes `tshark` to capture Wi-Fi packets on `mon0` for a specified duration or packet count, and saves the output as a `.pcap` file.

- **sniff_from_all_channels()**  
  Iterates through channels 1–13, setting the monitor interface to each channel and capturing packets, allowing for multi-channel analysis.

### 2. **PCAP Parser** (`pcap_parser.py`)
- **parse_network_beacon_pcaps(pcap_folder, network_name)**  
  Processes a folder of beacon `.pcap` files. Uses `beacon_pcap_parser` to extract beacon information, creates a pandas DataFrame, and saves the parsed data as CSV.

- **beacon_pcap_parser(pcap_file)**  
  Reads a single `.pcap` file with pyshark, extracts key fields from beacon frames (e.g., SSID, channel, RSSI), and returns a list of beacon packet dictionaries.

- **data_parser(pcap_file, ap_mac, dev_mac)**  
  Parses data frames matching a filter based on access point and device MAC addresses. Extracts fields such as retry flag, PHY type, MCS index, bandwidth, data rate, and timestamp, and returns a structured DataFrame.

### 3. **Performance Monitor** (`monitor.py`)
- **evaluate_throughput_df(df)**  
  Calculates throughput by using the cumulative count of retransmissions (via the retry flag) and computing the effective data rate as `data_rate * (1 - frame_loss_rate)`. This function adds a new column to the DataFrame.

- **aggregate_beacon_packets(network_files)**  
  Groups beacon data by SSID, RSSI, and channel from parsed CSV files, aggregates the counts, and saves the results for further density analysis.

- **monitor_network_density(network_files)**  
  Computes a density metric (RSSID) by summing the inverses of the absolute RSSI values across aggregated beacon frames and exports the results as a CSV file.

### 4. **Performance Analyzer** (`analyzer.py`)
- **add_rate_gap_to_df(df)**  
  Computes and appends a `rate_gap` column to the provided DataFrame. The `rate_gap` is determined by comparing the expected versus the actual data rate (using a helper function from an external module).

- **rate_gap_percentage(df)**  
  Calculates the percentage of packets with a non-zero rate gap, indicating performance issues or interference, and returns this as a DataFrame.

- **phy_type_percentage(df)**  
  Computes the distribution of PHY types present in the data and maps them to human-readable names using predefined mappings.

- **short_gi_percentage(df)**  
  Determines the percentage of packets using Short Guard Interval (short_gi), comparing rates between interfered and non-interfered packets.

- **general_statistics(df)**  
  Provides descriptive statistics (min, median, mean, 75th and 95th percentiles, and max) for key performance metrics such as RSSI, rate gap, throughput, and data rate.

- **export_statistics(df, folder_name)**  
  Creates a directory (if it doesn’t exist) and exports various performance statistics (rate gap percentage, PHY type distribution, short_gi statistics, and general statistics) into separate CSV files.

### 5. **Visualizer** (`visualizer.py`)
- This module is intended to visually represent the performance metrics computed by the monitor and analyzer modules.

---
## Prerequisites
  - **Install neccessary packages:** 
  `pip install -r requirements.txt`


## How to Run

1. **Capture packets (requires root)**:
   ```bash
   sudo python3 sniffer.py
   ```

2. **Analyze captured data**:
   Modify and run `main.py` with either:
   ```python
   network_density() //1.1
   data_analyze("NETWORK_NAME") //1.2
   ```

3. **View outputs**:
   - Statistics → `/statistics & /output` 
   - Plots → `/figures`

---

## Requirements

- Python 3.10+
- `pyshark`
- `pandas`, `numpy`, `matplotlib`
- `tshark` installed (and root access)

---

## Authors (Group 4)

- Nikolaos Papoutsakis  
- Argyris Christakis  
- Michalis Syrianos  
- Sokratis Siganos
