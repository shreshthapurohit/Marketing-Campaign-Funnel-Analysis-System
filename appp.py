import streamlit as st
import pandas as pd
import plotly.express as px
#import mysql.connector

#DATABASE CONNECTION
#conn = mysql.connector.connect(
#        host="localhost",
#       user="root",
#        password="k26121110s@",   # ← Your actual password
#        database="marketing_db",
#        use_pure=True              # ← Fixes connector errors
#   )
    
#cursor = conn.cursor()

#STREAMLIT UI
st.title("Marketing Funnel Analysis Dashboard")
#st.subheader("User Registration")

#username = st.text_input("Username")
#email = st.text_input("Email")
#password = st.text_input("Password", type="password")

#if st.button("Register"):
 
#query ="""INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"""
#cursor.execute(query, (username, email, password))
# conn.commit()
# st.success("User registered successfully!")

# ====================================================

st.set_page_config(
    page_title="Marketing Funnel Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# PREMIUM UI CSS
# =====================================================
st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

h1, h2, h3, h4 {
    color: white;
}

[data-testid="stMetric"] {
    background-color: #1E1E1E;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #333;
    text-align: center;
}

.stDownloadButton button {
    width: 100%;
    border-radius: 10px;
    height: 45px;
    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================
st.markdown("""
# 📊 Marketing Funnel Analysis Dashboard

### Smart Analytics • Dynamic CSV Upload • Insights Engine 🚀
""")

st.markdown("---")

# =====================================================
# FILE UPLOAD
# =====================================================
uploaded_file = st.file_uploader(
    "📂 Upload CSV Dataset",
    type=["csv"]
)

# =====================================================
# MAIN APP
# =====================================================
if uploaded_file:

    # LOAD DATA
    df = pd.read_csv(uploaded_file)

    st.success("✅ Dataset uploaded successfully!")

    # =================================================
    # DATA PREVIEW
    # =================================================
    with st.expander("🔍 Dataset Preview"):
        st.dataframe(df.head())

    st.markdown("---")

    # =================================================
    # COLUMN MAPPING
    # =================================================
    st.subheader("🧩 Column Mapping")

    columns = ["None"] + df.columns.tolist()

    col1, col2 = st.columns(2)

    with col1:
        impressions_col = st.selectbox(
            "Impressions Column",
            columns
        )

        clicks_col = st.selectbox(
            "Clicks Column",
            columns
        )

        leads_col = st.selectbox(
            "Leads Column",
            columns
        )

        conversions_col = st.selectbox(
            "Conversions Column",
            columns
        )

    with col2:
        revenue_col = st.selectbox(
            "Revenue Column",
            columns
        )

        channel_col = st.selectbox(
            "Channel Column",
            columns
        )

        audience_col = st.selectbox(
            "Audience Column",
            columns
        )

    st.markdown("---")

    # =================================================
    # DATA CLEANING
    # =================================================
    numeric_cols = []

    for col in [
        impressions_col,
        clicks_col,
        leads_col,
        conversions_col,
        revenue_col
    ]:

        if col != "None":
            numeric_cols.append(col)
            df[col] = pd.to_numeric(
                df[col],
                errors='coerce'
            )

    if numeric_cols:
        df[numeric_cols] = df[numeric_cols].fillna(0)

    # =================================================
    # SIDEBAR FILTERS
    # =================================================
    st.sidebar.title("🎛️ Filters")

    filtered_df = df.copy()

    if channel_col != "None":

        selected_channel = st.sidebar.multiselect(
            "Select Channel",
            options=df[channel_col].unique(),
            default=df[channel_col].unique()
        )

        filtered_df = filtered_df[
            filtered_df[channel_col].isin(
                selected_channel
            )
        ]

    if audience_col != "None":

        selected_audience = st.sidebar.multiselect(
            "Select Audience",
            options=df[audience_col].unique(),
            default=df[audience_col].unique()
        )

        filtered_df = filtered_df[
            filtered_df[audience_col].isin(
                selected_audience
            )
        ]

    # =================================================
    # CHECK EMPTY DATA
    # =================================================
    if filtered_df.empty:
        st.warning("⚠️ No data available after filtering")
        st.stop()

    # =================================================
    # METRICS CALCULATION
    # =================================================
    if (
        impressions_col != "None" and
        clicks_col != "None"
    ):
        filtered_df["CTR"] = (
            filtered_df[clicks_col] /
            filtered_df[impressions_col]
        )

    if (
        leads_col != "None" and
        clicks_col != "None"
    ):
        filtered_df["Lead_Rate"] = (
            filtered_df[leads_col] /
            filtered_df[clicks_col]
        )

    if (
        conversions_col != "None" and
        leads_col != "None"
    ):
        filtered_df["Conversion_Rate"] = (
            filtered_df[conversions_col] /
            filtered_df[leads_col]
        )

    filtered_df.replace(
        [float('inf'), -float('inf')],
        0,
        inplace=True
    )

    # =================================================
    # KPI CARDS
    # =================================================
    st.markdown("## 📌 Key Performance Indicators")

    k1, k2, k3, k4 = st.columns(4)

    if revenue_col != "None":
        k1.metric(
            "💰 Revenue",
            f"{int(filtered_df[revenue_col].sum()):,}"
        )

    if clicks_col != "None":
        k2.metric(
            "🖱️ Clicks",
            f"{int(filtered_df[clicks_col].sum()):,}"
        )

    if leads_col != "None":
        k3.metric(
            "📞 Leads",
            f"{int(filtered_df[leads_col].sum()):,}"
        )

    if conversions_col != "None":
        k4.metric(
            "✅ Conversions",
            f"{int(filtered_df[conversions_col].sum()):,}"
        )

    st.markdown("---")

    # =================================================
    # FUNNEL ANALYSIS
    # =================================================
    funnel_stages = []
    funnel_values = []

    if impressions_col != "None":
        funnel_stages.append("Impressions")
        funnel_values.append(filtered_df[impressions_col].sum())

    if clicks_col != "None":
        funnel_stages.append("Clicks")
        funnel_values.append(filtered_df[clicks_col].sum())

    if leads_col != "None":
        funnel_stages.append("Leads")
        funnel_values.append(filtered_df[leads_col].sum())

    if conversions_col != "None":
        funnel_stages.append("Conversions")
        funnel_values.append(filtered_df[conversions_col].sum())

    if len(funnel_stages) >= 2:
        st.markdown("## 🔻 Funnel Analysis")

        funnel_data = pd.DataFrame({
            "Stage": funnel_stages,
            "Value": funnel_values
        })

        funnel_fig = px.funnel(
            funnel_data,
            x="Value",
            y="Stage"
        )

        st.plotly_chart(
            funnel_fig,
            use_container_width=True
        )
    elif len(funnel_stages) == 1:
        st.warning("Select at least two funnel columns to display the funnel chart.")
    else:
        st.info("Funnel chart requires at least one funnel column selection.")

    # =================================================
    # CHANNEL PERFORMANCE
    # =================================================
    if (
        channel_col != "None" and
        revenue_col != "None"
    ):

        st.markdown("## 📈 Channel Performance")

        channel_perf = (
            filtered_df
            .groupby(channel_col)[revenue_col]
            .sum()
            .reset_index()
        )

        bar_fig = px.bar(
            channel_perf,
            x=channel_col,
            y=revenue_col,
            text_auto=True
        )

        st.plotly_chart(
            bar_fig,
            use_container_width=True
        )

        # PIE CHART
        st.markdown("## 🥧 Revenue Distribution")

        pie_fig = px.pie(
            channel_perf,
            names=channel_col,
            values=revenue_col
        )

        st.plotly_chart(
            pie_fig,
            use_container_width=True
        )

    # =================================================
    # SMART INSIGHTS
    # =================================================
    st.markdown("## 💡 Smart Insights")

    if (
        channel_col != "None" and
        revenue_col != "None"
    ):

        best_channel = (
            channel_perf
            .sort_values(
                by=revenue_col,
                ascending=False
            )
            .iloc[0][channel_col]
        )

        st.success(
            f"🏆 Best Performing Channel: {best_channel}"
        )

    if "CTR" in filtered_df.columns:

        avg_ctr = filtered_df["CTR"].mean()

        st.info(
            f"📊 Average CTR: {avg_ctr:.2f}"
        )

        if avg_ctr < 0.05:
            st.warning(
                "⚠️ CTR is low. Improve marketing creatives."
            )

    if "Conversion_Rate" in filtered_df.columns:

        avg_conversion = (
            filtered_df["Conversion_Rate"].mean()
        )

        st.info(
            f"🎯 Average Conversion Rate: {avg_conversion:.2f}"
        )

        if avg_conversion < 0.10:
            st.warning(
                "⚠️ Conversion rate is low. Optimize landing pages."
            )

    # =================================================
    # EXPORT FEATURE
    # =================================================
    st.markdown("## 📥 Export Analysis")

    csv = filtered_df.to_csv(index=False)

    st.download_button(
        label="⬇️ Download Filtered Dataset",
        data=csv,
        file_name="marketing_analysis.csv",
        mime="text/csv"
    )

    # =================================================
    # FINAL SUCCESS
    # =================================================
    st.success("✅ Analysis Completed Successfully!")
