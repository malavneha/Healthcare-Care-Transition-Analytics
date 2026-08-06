import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Healthcare Care Transition Analytics",
    layout="wide"
)

st.title("🏥 Healthcare Care Transition Analytics Dashboard")

# ----------------------------
# Upload Dataset
# ----------------------------
uploaded_file = st.file_uploader(
    "Upload HHS_Unaccompanied_Alien_Children_Program.csv",
    type=["csv"]
)

if uploaded_file is not None:

    # ----------------------------
    # Read Dataset
    # ----------------------------
    df = pd.read_csv(uploaded_file)

    # Convert Date
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Convert Numeric Columns
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

        df[col] = pd.to_numeric(df[col], errors="coerce")

    # ----------------------------
    # Handle Missing Values
    # ----------------------------
    df.fillna(0, inplace=True)

    # ----------------------------
    # Calculate KPIs
    # ----------------------------
    df["Transfer Efficiency Ratio"] = np.where(
        df["Children apprehended and placed in CBP custody*"] > 0,
        df["Children transferred out of CBP custody"] /
        df["Children apprehended and placed in CBP custody*"],
        np.nan
    )

    df["Discharge Efficiency Ratio"] = np.where(
        df["Children in HHS Care"] > 0,
        df["Children discharged from HHS Care"] /
        df["Children in HHS Care"],
        np.nan
    )

    # ----------------------------
    # Dataset Preview
    # ----------------------------
    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # ----------------------------
    # KPI Cards
    # ----------------------------
    st.subheader("Key Performance Indicators")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Average Transfer Efficiency",
            f"{df['Transfer Efficiency Ratio'].mean():.2%}"
        )

    with col2:
        st.metric(
            "Average Discharge Efficiency",
            f"{df['Discharge Efficiency Ratio'].mean():.2%}"
        )

    # ----------------------------
    # Monthly Apprehension Chart
    # ----------------------------
    st.subheader("Monthly Apprehensions")

    monthly = (
        df.groupby(df["Date"].dt.to_period("M"))[
            "Children apprehended and placed in CBP custody*"
        ]
        .sum()
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    monthly.plot(ax=ax)

    ax.set_xlabel("Month")
    ax.set_ylabel("Children")
    ax.set_title("Monthly Apprehensions")

    st.pyplot(fig)

else:
    st.info("👆 Please upload the HHS_Unaccompanied_Alien_Children_Program.csv file to begin.")
