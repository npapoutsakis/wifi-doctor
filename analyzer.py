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


# Maybe statistics for all?
def export_statistics(df: pd.DataFrame, folder_name: str):
    folder_path = f"./statistics/{folder_name}"
    os.makedirs(f"{folder_path}", exist_ok=True)

    stats_df = rate_gap_percentage(df)
    stats_df.to_csv(f"./{folder_path}/{folder_name}_rate_gap.csv", index=False)

    stats_df = phy_type_percentage(df)
    stats_df.to_csv(f"./{folder_path}/{folder_name}_phy_type.csv", index=False)


# What arguement?
def common_statistics():
    return
