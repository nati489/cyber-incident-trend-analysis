"""
Main entry point for the cyber incidents analysis project.

Runs the pipeline:
1) Load + prep data
2) Layer 2: descriptive stats + YoY %
3) Layer 3: unusual-year detection (z-scores)
4) Charts saved to PNG
5) Auto report saved to report.md
"""

from data_loader import load_incidents
from analysis_layer2 import yearly_summary, year_over_year_change
from analysis_layer3 import zscore_flags, print_flags
from charts import plot_year_trend, plot_top_types
from analysis_layer4 import write_report_md


def main():
    csv_path = "eurepoc_global_dataset_1_3.csv"

    # ---------- Load ----------
    df = load_incidents(csv_path)

    # ---------- Layer 2 ----------
    print("\n===== Yearly incident baseline =====")
    year_counts = yearly_summary(df)

    print("\n===== Year-to-year % change =====")
    yoy = year_over_year_change(year_counts)
    print(yoy.round(2))

    # ---------- Layer 3 ----------
    z_threshold = 2.0
    z_table = zscore_flags(year_counts, threshold=z_threshold)
    print_flags(z_table, threshold=z_threshold)

    # ---------- Charts ----------
    plot_year_trend(year_counts)
    plot_top_types(df, top_n=10)

    # ---------- Report ----------
    write_report_md(
        out_path="report.md",
        df=df,
        year_counts=year_counts,
        yoy=yoy,
        z_table=z_table,
        z_threshold=z_threshold,
        top_n_types=5
    )
    print("Saved report: report.md")


if __name__ == "__main__":
    main()
