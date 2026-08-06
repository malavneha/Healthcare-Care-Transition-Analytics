import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Healthcare Care Transition Analytics", layout="wide")

st.title("🏥 Healthcare Care Transition Analytics Dashboard")

uploaded_file = st.file_uploader(
    "Upload HHS_Unaccompanied_Alien_Children_Program.csv",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

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

    st.subheader("Dataset Preview")
    st.dataframe(df.head())
