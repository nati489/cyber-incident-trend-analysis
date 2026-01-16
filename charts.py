"""
Charts for the project.
"""

import pandas as pd
import matplotlib.pyplot as plt


def plot_year_trend(year_counts: pd.Series, out_path: str = "incidents_per_year.png") -> None:
    # Drop missing years so the line plot doesn’t break
    year_counts = year_counts.dropna()

    # Simple line plot to show how incidents change over time
    plt.figure()
    year_counts.plot(kind="line")
    plt.title("Cyber incidents per year (start_date)")
    plt.xlabel("Year")
    plt.ylabel("Number of incidents")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.show()


def plot_top_types(df: pd.DataFrame, top_n=10, out_path="top_incident_types.png") -> None:
    # Count the most common incident types and keep the top N
    counts = df["incident_type"].value_counts().head(top_n)

    # Bigger figure + horizontal bars makes long labels easier to read
    plt.figure(figsize=(12, 6))
    counts.sort_values().plot(kind="barh")

    plt.title(f"Top {top_n} incident types")
    plt.xlabel("Count")
    plt.ylabel("Incident type")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.show()
