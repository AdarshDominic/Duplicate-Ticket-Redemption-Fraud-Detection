import pandas as pd
import streamlit as st

st.title("Duplicate Ticket Redemption - Fraud Dashboard")

# Load your exported CSV
df = pd.read_csv("fraud_ops_alerts.csv")

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Alerts", len(df))
col2.metric("High Risk Alerts", (df["final_risk_level"] == "HIGH").sum())
col3.metric("Total Overpayment (£)", round(df["overpayment_amount"].sum(), 2))
col4.metric("Avg Time Gap (sec)", round(df["time_gap_seconds"].mean(), 2))

# Filters
risk = st.multiselect(
    "Risk Level",
    df["final_risk_level"].unique(),
    default=list(df["final_risk_level"].unique())
)

filtered = df[df["final_risk_level"].isin(risk)]

st.subheader("Alerts by Risk Level")
st.bar_chart(filtered["final_risk_level"].value_counts())

st.subheader("Top Risky Customers")
top_customers = (
    filtered.groupby("customer_id")["final_risk_score"]
    .max()
    .sort_values(ascending=False)
    .head(10)
)
st.dataframe(top_customers)

st.subheader("Alert Details")
st.dataframe(filtered.sort_values("final_risk_score", ascending=False))
