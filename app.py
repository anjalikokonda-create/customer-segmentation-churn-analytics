import streamlit as st
import pandas as pd

df = pd.read_csv("data/Churn_Modelling.csv")

st.title("Customer Segmentation & Churn Analytics")

# KPIs
total_customers = len(df)
churned = df['Exited'].sum()
churn_rate = round(df['Exited'].mean()*100, 2)

col1, col2, col3 = st.columns(3)

col1.metric("Total Customers", total_customers)
col2.metric("Churned Customers", churned)
col3.metric("Churn Rate", f"{churn_rate}%")