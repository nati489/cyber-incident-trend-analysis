"""
Load the cyber incident dataset for analysis (mainly: parse dates, add a year column).
"""

import pandas as pd


def load_incidents(csv_path: str) -> pd.DataFrame:
    # Read the CSV into a DataFrame
    df = pd.read_csv(csv_path)

    # Anything that can’t be parsed turns into NaT instead of crashing
    df["start_date"] = pd.to_datetime(
        df["start_date"],
        errors="coerce",
        dayfirst=True
    )

    # Pull out just the year since that’s all we need for the trend analysis
    df["year"] = df["start_date"].dt.year

    return df
