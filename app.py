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
