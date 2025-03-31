import os
import numpy as np
import pandas as pd
from data_packet import DataPacket
from rate_gap import rate_gap
from field_mappings import *


def add_rate_gap_to_df(df: pd.DataFrame):

    rate_gap_arr = rate_gap(df)
    df["rate_gap"] = rate_gap_arr

    # return rate_gap_arr


"""
    Statistics of analyzer
"""


# EXPORT ALL RATE_GAPS AS PERCENTAGES
# WE WANT TO SHOW THAT 15 IS 97.8%
def rate_gap_percentage(df: pd.DataFrame):
    rate_gap_count = (df["rate_gap"] > 0).sum()
    percentage = round((rate_gap_count / len(df)) * 100, 4)
    stats_df = pd.DataFrame({"percentage": [f"{percentage}%"]})

    return stats_df.copy()


def phy_type_percentage(df: pd.DataFrame):
    stats_df = df["phy"].value_counts(normalize=True) * 100
    stats_df = stats_df.reset_index()
    stats_df.columns = ["phy_type", "percentage"]
    stats_df["phy_type"] = stats_df["phy_type"].map(lambda x: phy_type_mapping[x])

    return stats_df.copy()


def short_gi_percentage(df: pd.DataFrame):

    non_rate_gap_arr = df[["short_gi"]][
        df["rate_gap"] == 0
    ].values  # rate_gap = 0 -> non-interfered packets
    rate_gap_arr = df[["short_gi"]][
        df["rate_gap"] > 0
    ].values  # rate_gap > 0 -> interfered packets

    total_perc = (df["short_gi"] == True).mean() * 100
    non_interf_perc = (non_rate_gap_arr == True).sum() / len(non_rate_gap_arr) * 100
    interf_perc = (rate_gap_arr == True).sum() / len(rate_gap_arr) * 100
    stats_df = pd.DataFrame(
        {
            "columns": ["all", "non-interference", "interference"],
            "short_gi_true_percentage": [total_perc, non_interf_perc, interf_perc],
        }
    )

    return stats_df.copy()


def general_statistics(df: pd.DataFrame):
    columns = ["rssi", "rate_gap", "throughput", "data_rate"]
    stats_df = pd.DataFrame(
        {
            "column": columns,
            "min": df[columns].min().map(lambda x: round(x, 4)),
            "median": df[columns].median().map(lambda x: round(x, 4)),
            "mean": df[columns].mean().map(lambda x: round(x, 4)),
            "75p": df[columns].quantile(0.75).map(lambda x: round(x, 4)),  # 75p
            "95p": df[columns].quantile(0.95).map(lambda x: round(x, 4)),  # 95p
            "max": df[columns].max().map(lambda x: round(x, 4)),
        }
    )
    return stats_df.copy()


# Maybe statistics for all?
def export_statistics(df: pd.DataFrame, folder_name: str):
    folder_path = f"./statistics/{folder_name}"
    os.makedirs(f"{folder_path}", exist_ok=True)

    stats_df = rate_gap_percentage(df)
    stats_df.to_csv(f"./{folder_path}/{folder_name}_rate_gap.csv", index=False)

    stats_df = phy_type_percentage(df)
    stats_df.to_csv(f"./{folder_path}/{folder_name}_phy_type.csv", index=False)

    stats_df = short_gi_percentage(df)
    stats_df.to_csv(f"./{folder_path}/{folder_name}_short_gi.csv", index=False)

    stats_df = general_statistics(df)
    stats_df.to_csv(
        f"./{folder_path}/{folder_name}_general_statistics.csv", index=False
    )


# What arguement?
def common_statistics():
    return
