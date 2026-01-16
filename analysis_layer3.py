"""
Layer 3: simple anomaly detection on yearly counts using z-scores.
"""

import pandas as pd


def zscore_flags(year_counts: pd.Series, threshold: float = 2.0) -> pd.DataFrame:
    # Drop missing values and force float so the math works properly
    s = year_counts.dropna().astype(float)

    # Mean and standard deviation for the baseline
    mean = s.mean()
    std = s.std()

    # If everything is the same value, std will be 0
    if std == 0:
        out = pd.DataFrame({
            "count": s,
            "z": 0.0,
            "flag": False
        })
        return out

    # Z-score tells us how far each year is from the average
    z = (s - mean) / std

    # Flag years that are far enough away from the mean
    flagged = z.abs() >= threshold

    # Put everything into a single table for easier inspection
    out = pd.DataFrame({
        "count": s.astype(int),
        "z": z.round(2),
        "flag": flagged
    })

    return out


def print_flags(z_table: pd.DataFrame, threshold: float) -> None:
    # Simple header so the output is easy to read in the terminal
    print("===== Layer 3: Unusual-year detection (z-scores) =====")
    print(f"Rule: |z| >= {threshold} counts as unusual\n")

    # Keep only the rows that were flagged as unusual
    flagged = z_table[z_table["flag"]].copy()

    # If nothing was flagged, say so and stop early
    if flagged.empty:
        print("No unusual years flagged at this threshold.\n")
        return

    # Sort by how extreme the z-score is (most unusual first)
    flagged = flagged.reindex(
        flagged["z"].abs().sort_values(ascending=False).index
    )

    print("Flagged years:")
    for year, row in flagged.iterrows():
        # Year comes from the index, counts and z from the row
        print(f"- {int(year)}: {int(row['count'])} incidents (z = {row['z']})")

    print()
