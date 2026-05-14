Marketing Campaign Funnel Analysis

Overview

This project is a Streamlit analytics dashboard for marketing campaign performance. It supports CSV upload, interactive column mapping, funnel visualization, KPI cards, channel performance charts, and smart insights.

---

Features

- Upload CSV dataset from any marketing campaign
- Interactive column mapping for Impressions, Clicks, Leads, Conversions, Revenue, Channel, and Audience
- KPI Dashboard for revenue, clicks, leads, and conversions
- Funnel visualization with optional stages (e.g. Impressions → Clicks → Conversions)
- Channel performance bar and pie charts
- Sidebar filters for channel and audience
- Export filtered dataset as CSV

---

Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   streamlit run appp.py
   ```
3. Upload a CSV file and map the required columns.

Note: The funnel chart works if at least two funnel stages are selected. `Leads` is optional if your dataset does not include it.

---

Tech Stack

- Python
- Streamlit
- Pandas
- Plotly

---

Insights Generated

- Best performing channel identification
- Average CTR and conversion rate
- Funnel stage drop-off detection
- Data-driven recommendations based on performance thresholds

