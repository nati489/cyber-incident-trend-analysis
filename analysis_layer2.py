"""
Layer 2: descriptive statistics + simple year-to-year change.

This layer answers:
- What does a "typical" year look like?
- How much do counts vary between years?
- How fast does it change year to year?
"""

import pandas as pd


def yearly_summary(df: pd.DataFrame) -> pd.Series:
    """
    Builds the yearly incident count series and prints a quick baseline summary.
    Returns:
        pd.Series indexed by year -> count
    """
    # Count how many incidents happened in each year
    year_counts = df["year"].dropna().value_counts().sort_index()

    # Get the range of years covered in the dataset
    start_year = int(year_counts.index.min())
    end_year = int(year_counts.index.max())

    # Basic descriptive stats to understand what a "normal" year looks like
    avg = year_counts.mean()
    med = year_counts.median()
    sd = year_counts.std()

    # Find the years with the lowest and highest number of incidents
    low_year = int(year_counts.idxmin())
    high_year = int(year_counts.idxmax())

    low_val = int(year_counts.min())
    high_val = int(year_counts.max())

    # Print a short summary so we can quickly see the baseline in the terminal
    print(f"Years covered: {start_year}–{end_year}")
    print(f"Average per year: {avg:.2f}")
    print(f"Median per year: {med:.2f}")
    print(f"Std dev: {sd:.2f}")
    print(f"Lowest year: {low_year} ({low_val} incidents)")
    print(f"Highest year: {high_year} ({high_val} incidents)")

    return year_counts


def year_over_year_change(year_counts: pd.Series) -> pd.Series:
    """
    Percent change from the previous year.
    """
    # Convert to float so percent change works correctly
    year_counts = year_counts.astype(float)

    # pct_change() compares each year to the previous one
    return year_counts.pct_change() * 100
