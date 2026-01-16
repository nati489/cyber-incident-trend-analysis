# Cyber Incident Trend Analysis (2000–2024)

## Overview
This project analyzes global cyber incident data to identify long-term trends, sudden spikes, and the types of incidents driving those spikes. Using real-world data from the **EU RepoC (European Repository of Cyber Incidents)**, the project combines statistical analysis with Python scripting to produce reproducible results, visualizations, and an automated written report.

The focus of the project is not just visualization, but **quantitative reasoning**: detecting unusually high-activity years using statistics and explaining *what* drove those increases.

---

## Project Structure
cyber-incident-trend-analysis/
│
├── analysis_layer2.py
├── analysis_layer3.py
├── analysis_layer4.py
├── charts.py
├── data_loader.py
├── main.py
├── README.md
├── report.md
├── europec_global_dataset_1_3.csv
├── incidents_per_year.png
└── top_incident_types.png



Each file has a single responsibility, making the codebase easy to understand and extend.

---

## Methods Used
- Descriptive statistics (mean, median, standard deviation)
- Year-over-year percentage change
- Z-score anomaly detection (|z| ≥ 2)
- Incident-type breakdown for spike years
- Automated Markdown report generation
- Matplotlib visualizations

---

Full results and breakdowns are available in the auto-generated `report.md`.

---

## How to Run

1. Make sure Python 3 is installed

2. Install dependencies:

```bash
pip install pandas matplotlib

Run the analysis:

python main.py


Running the script will:

- print statistical summaries to the terminal

- generate charts

- create or update report.md
