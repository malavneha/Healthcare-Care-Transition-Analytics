import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Healthcare Care Transition Analytics",
    page_icon="🏥",
    layout="wide"
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("🏥 Healthcare Care Transition Analytics Dashboard")

st.markdown("""
Analyze the efficiency of the **Unaccompanied Alien Children (UAC)** care transition pipeline.

This dashboard provides operational insights into:

- CBP Apprehensions
- CBP Custody
- Transfers to HHS
- Children in HHS Care
- Discharges from HHS Care
""")

st.divider()

# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------
uploaded_file = st.file_uploader(
    "📂 Upload HHS_Unaccompanied_Alien_Children_Program.csv",
    type=["csv"]
)

if uploaded_file is not None:

    # -----------------------------
    # Load Data
    # -----------------------------
    df = pd.read_csv(uploaded_file)

    # -----------------------------
    # Convert Date
    # -----------------------------
    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    # -----------------------------
    # Numeric Columns
    # -----------------------------
    numeric_cols = [
        "Children apprehended and placed in CBP custody*",
        "Children in CBP custody",
        "Children transferred out of CBP custody",
        "Children in HHS Care",
        "Children discharged from HHS Care"
    ]

    for col in numeric_cols:

        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
        )

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    # Fill only numeric columns
    df[numeric_cols] = df[numeric_cols].fillna(0)

    # --------------------------------------------------
    # SIDEBAR
    # --------------------------------------------------

    st.sidebar.header("📅 Dashboard Filters")

    start_date = st.sidebar.date_input(
        "Start Date",
        value=df["Date"].min().date()
    )

    end_date = st.sidebar.date_input(
        "End Date",
        value=df["Date"].max().date()
    )

    filtered_df = df[
        (df["Date"] >= pd.to_datetime(start_date))
        &
        (df["Date"] <= pd.to_datetime(end_date))
    ]
        # --------------------------------------------------
    # KPI CALCULATIONS
    # --------------------------------------------------

    filtered_df["Transfer Efficiency Ratio"] = np.where(
        filtered_df["Children apprehended and placed in CBP custody*"] > 0,
        filtered_df["Children transferred out of CBP custody"] /
        filtered_df["Children apprehended and placed in CBP custody*"],
        np.nan
    )

    filtered_df["Discharge Efficiency Ratio"] = np.where(
        filtered_df["Children in HHS Care"] > 0,
        filtered_df["Children discharged from HHS Care"] /
        filtered_df["Children in HHS Care"],
        np.nan
    )

    # --------------------------------------------------
    # KPI VALUES
    # --------------------------------------------------

    total_apprehended = int(
        filtered_df["Children apprehended and placed in CBP custody*"].sum()
    )

    total_transferred = int(
        filtered_df["Children transferred out of CBP custody"].sum()
    )

    avg_hhs = int(
        filtered_df["Children in HHS Care"].mean()
    )

    total_discharged = int(
        filtered_df["Children discharged from HHS Care"].sum()
    )

    avg_transfer = (
        filtered_df["Transfer Efficiency Ratio"]
        .replace([np.inf, -np.inf], np.nan)
        .mean()
    )

    avg_discharge = (
        filtered_df["Discharge Efficiency Ratio"]
        .replace([np.inf, -np.inf], np.nan)
        .mean()
    )

    # --------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------

    st.subheader("📊 Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "👧 Total Apprehended",
        f"{total_apprehended:,}"
    )

    col2.metric(
        "🚍 Total Transfers",
        f"{total_transferred:,}"
    )

    col3.metric(
        "🏥 Avg. Children in HHS Care",
        f"{avg_hhs:,}"
    )

    col4.metric(
        "🏠 Total Discharges",
        f"{total_discharged:,}"
    )

    col5, col6 = st.columns(2)

    col5.metric(
        "📈 Avg Transfer Ratio",
        f"{avg_transfer:.2%}"
    )

    col6.metric(
        "📉 Avg Discharge Ratio",
        f"{avg_discharge:.2%}"
    )

    st.divider()
        # --------------------------------------------------
    # CHARTS
    # --------------------------------------------------

    st.subheader("📈 Dashboard Visualizations")

    left, right = st.columns(2)

    # -----------------------------
    # Monthly Apprehensions
    # -----------------------------
    monthly_app = (
        filtered_df.groupby(filtered_df["Date"].dt.to_period("M"))[
            "Children apprehended and placed in CBP custody*"
        ]
        .sum()
        .reset_index()
    )

    monthly_app["Date"] = monthly_app["Date"].astype(str)

    fig1 = px.line(
        monthly_app,
        x="Date",
        y="Children apprehended and placed in CBP custody*",
        title="Monthly Apprehensions",
        markers=True
    )

    left.plotly_chart(fig1, use_container_width=True)

    # -----------------------------
    # Monthly Transfers
    # -----------------------------
    monthly_transfer = (
        filtered_df.groupby(filtered_df["Date"].dt.to_period("M"))[
            "Children transferred out of CBP custody"
        ]
        .sum()
        .reset_index()
    )

    monthly_transfer["Date"] = monthly_transfer["Date"].astype(str)

    fig2 = px.line(
        monthly_transfer,
        x="Date",
        y="Children transferred out of CBP custody",
        title="Monthly Transfers",
        markers=True
    )

    right.plotly_chart(fig2, use_container_width=True)

    # -----------------------------
    # Monthly Discharges
    # -----------------------------
    left2, right2 = st.columns(2)

    monthly_discharge = (
        filtered_df.groupby(filtered_df["Date"].dt.to_period("M"))[
            "Children discharged from HHS Care"
        ]
        .sum()
        .reset_index()
    )

    monthly_discharge["Date"] = monthly_discharge["Date"].astype(str)

    fig3 = px.line(
        monthly_discharge,
        x="Date",
        y="Children discharged from HHS Care",
        title="Monthly Discharges",
        markers=True
    )

    left2.plotly_chart(fig3, use_container_width=True)

    # -----------------------------
    # CBP vs HHS Comparison
    # -----------------------------
    comparison = pd.DataFrame({
        "Category": [
            "CBP Custody",
            "HHS Care"
        ],
        "Children": [
            filtered_df["Children in CBP custody"].mean(),
            filtered_df["Children in HHS Care"].mean()
        ]
    })

    fig4 = px.bar(
        comparison,
        x="Category",
        y="Children",
        title="Average Children: CBP vs HHS"
    )

    right2.plotly_chart(fig4, use_container_width=True)

    st.divider()
