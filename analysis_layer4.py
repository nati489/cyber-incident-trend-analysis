"""
Layer 4: turn results into a clean, readable report (report.md).

This file takes the outputs from earlier layers and writes:
- baseline stats
- year-to-year change highlights
- flagged unusual years (z-scores)
- top incident types inside the spike years
- a few plain-English conclusions
"""

from __future__ import annotations

import pandas as pd


def _format_int(x) -> str:
    # Small helper so years show up nicely in the markdown (
    try:
        return f"{int(x)}"
    except Exception:
        return str(x)


def _top_types_for_year(df: pd.DataFrame, year: int, top_n: int = 5) -> pd.Series:
    # Grab only the rows from that year, then count the incident types
    subset = df[df["year"] == year]
    return subset["incident_type"].value_counts().head(top_n)


def write_report_md(
    out_path: str,
    df: pd.DataFrame,
    year_counts: pd.Series,
    yoy: pd.Series,
    z_table: pd.DataFrame,
    z_threshold: float = 2.0,
    top_n_types: int = 5
) -> None:
    # Basic cleanup so we don’t get weird NaNs in the report
    year_counts = year_counts.dropna()
    yoy = yoy.dropna()
    z_table = z_table.copy()

    # --- Baseline stats ---
    start_year = int(year_counts.index.min())
    end_year = int(year_counts.index.max())

    mean_val = year_counts.mean()
    med_val = year_counts.median()
    std_val = year_counts.std()

    low_year = int(year_counts.idxmin())
    high_year = int(year_counts.idxmax())
    low_count = int(year_counts.min())
    high_count = int(year_counts.max())

    # --- Biggest YoY jumps (just showing the biggest increases) ---
    yoy_increases = yoy.sort_values(ascending=False).head(5)

    # --- Pull out flagged years from the z-score table ---
    flagged = z_table[z_table["flag"]].copy()

    # Sometimes the year index can end up as floats, so convert back if possible
    try:
        flagged.index = flagged.index.astype(int)
    except Exception:
        pass

    flagged_years = list(flagged.index)

    # For each flagged year, find what incident types were most common
    flagged_types = {}
    for y in flagged_years:
        flagged_types[y] = _top_types_for_year(df, int(y), top_n=top_n_types)

    # --- Auto conclusions ---
    conclusions = []
    if flagged_years:
        conclusions.append(
            f"Unusual spike years were detected using z-scores (|z| ≥ {z_threshold}). "
            f"Flagged: {', '.join(str(y) for y in flagged_years)}."
        )
    else:
        conclusions.append(
            f"No years crossed the unusual threshold (|z| ≥ {z_threshold}) based on the yearly baseline."
        )

    # Quick “recent change” summary using the latest year (if we have enough data)
    if len(year_counts) >= 5:
        last_year = int(year_counts.index.max())
        prev_year = int(year_counts.index.max() - 1) if (year_counts.index.max() - 1) in year_counts.index else None
        if prev_year is not None:
            change = yoy.get(prev_year + 1, None)
            if change is not None:
                conclusions.append(
                    f"Most recent change: {prev_year} → {last_year} was {change:.2f}%."
                )

    # One more conclusion: biggest YoY increase overall (from the top 5 list)
    if not yoy_increases.empty:
        biggest_year = int(yoy_increases.index[0])
        biggest_val = float(yoy_increases.iloc[0])
        conclusions.append(
            f"Largest year-to-year increase was in {biggest_year}: {biggest_val:.2f}%."
        )

    # --- Build the markdown file line-by-line (easy to control formatting) ---
    lines = []
    lines.append("# Cyber Incident Trend Report")
    lines.append("")
    lines.append("This report was generated automatically by the project pipeline.")
    lines.append("")

    # Baseline section
    lines.append("## 1) Baseline (Yearly Counts)")
    lines.append(f"- Years covered: **{start_year}–{end_year}**")
    lines.append(f"- Mean incidents/year: **{mean_val:.2f}**")
    lines.append(f"- Median incidents/year: **{med_val:.2f}**")
    lines.append(f"- Standard deviation: **{std_val:.2f}**")
    lines.append(f"- Lowest year: **{low_year}** ({low_count} incidents)")
    lines.append(f"- Highest year: **{high_year}** ({high_count} incidents)")
    lines.append("")

    # YoY highlights
    lines.append("## 2) Biggest Year-to-Year Increases")
    if yoy_increases.empty:
        lines.append("- (No year-to-year changes available)")
    else:
        for year, val in yoy_increases.items():
            lines.append(f"- **{_format_int(year)}**: **{val:.2f}%**")
    lines.append("")

    # Unusual years
    lines.append("## 3) Unusual Years (Z-Score Flags)")
    lines.append(f"Rule used: **|z| ≥ {z_threshold}**")
    if flagged.empty:
        lines.append("- No years were flagged as unusual.")
    else:
        for y, row in flagged.iterrows():
            lines.append(f"- **{int(y)}**: {int(row['count'])} incidents (z = {row['z']})")
    lines.append("")

    # What drove the spike 
    lines.append("## 4) What Drove the Spike? (Top Incident Types in Flagged Years)")
    if not flagged_years:
        lines.append("- No flagged years → skipping breakdown.")
    else:
        for y in flagged_years:
            lines.append(f"### {int(y)}")
            top_types = flagged_types.get(y)
            if top_types is None or top_types.empty:
                lines.append("- (No incident types found for this year)")
            else:
                for t, c in top_types.items():
                    lines.append(f"- {t}: {int(c)}")
            lines.append("")
    lines.append("")

    # Conclusions
    lines.append("## 5) Conclusions (Auto-Summary)")
    for c in conclusions[:5]:
        lines.append(f"- {c}")
    lines.append("")

    # Just reminding what files the pipeline outputs
    lines.append("## 6) Generated Files")
    lines.append("- `incidents_per_year.png`")
    lines.append("- `top_incident_types.png`")
    lines.append("- `report.md`")
    lines.append("")

    # Write the markdown out to disk
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
