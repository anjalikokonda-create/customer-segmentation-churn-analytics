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
import matplotlib.pyplot as plt
import seaborn as sns

st.subheader("Geography-wise Churn Rate")

geo_churn = df.groupby('Geography')['Exited'].mean()*100

fig, ax = plt.subplots(figsize=(6,4))
geo_churn.plot(kind='bar', ax=ax)

ax.set_ylabel("Churn Rate (%)")
ax.set_title("Churn Rate by Geography")

st.pyplot(fig)
# Age Group Analysis

st.subheader("Age Group Churn Analysis")

df['AgeGroup'] = pd.cut(
    df['Age'],
    bins=[0,30,45,60,100],
    labels=['<30','30-45','46-60','60+']
)

age_churn = df.groupby('AgeGroup')['Exited'].mean()*100

fig, ax = plt.subplots(figsize=(6,4))

age_churn.plot(kind='bar', ax=ax)

ax.set_ylabel("Churn Rate (%)")
ax.set_title("Churn Rate by Age Group")

st.pyplot(fig)
# Sidebar Filter

st.sidebar.header("Filters")

country = st.sidebar.selectbox(
    "Select Geography",
    df['Geography'].unique()
)

filtered_df = df[df['Geography'] == country]

st.subheader(f"Customer Data - {country}")

st.dataframe(filtered_df.head(20))
st.sidebar.header("Filter Data")

geo_filter = st.sidebar.multiselect(
    "Select Geography",
    df["Geography"].unique(),
    default=df["Geography"].unique()
)

gender_filter = st.sidebar.multiselect(
    "Select Gender",
    df["Gender"].unique(),
    default=df["Gender"].unique()
)

df = df[
    (df["Geography"].isin(geo_filter)) &
    (df["Gender"].isin(gender_filter))
]
st.subheader("Balance vs Churn Analysis")

fig, ax = plt.subplots(figsize=(6,4))

ax.scatter(df["Balance"], df["Exited"], alpha=0.3)

ax.set_xlabel("Balance")
ax.set_ylabel("Exited (0 = No, 1 = Yes)")
ax.set_title("Balance vs Churn")

st.pyplot(fig)
st.subheader("Average Balance by Churn Status")

balance_churn = df.groupby("Exited")["Balance"].mean()

fig, ax = plt.subplots(figsize=(5,4))

balance_churn.plot(kind="bar", ax=ax)

ax.set_xticklabels(["Not Churned", "Churned"], rotation=0)
ax.set_ylabel("Average Balance")
ax.set_title("Balance Comparison")

st.pyplot(fig)
st.subheader("High-Value Customer Churn Analysis")

high_value = filtered_df[
    filtered_df['Balance'] > filtered_df['Balance'].median()
]

high_value_churn = round(high_value['Exited'].mean()*100, 2)

st.metric(
    "High-Value Customer Churn Rate",
    f"{high_value_churn}%"
)
st.subheader("Tenure-wise Churn Analysis")

filtered_df['TenureGroup'] = pd.cut(
    filtered_df['Tenure'],
    bins=[-1,3,7,10],
    labels=['New','Mid-Term','Long-Term']
)

tenure_churn = filtered_df.groupby('TenureGroup')['Exited'].mean()*100

fig, ax = plt.subplots(figsize=(6,4))
tenure_churn.plot(kind='bar', ax=ax)

ax.set_ylabel("Churn Rate (%)")
ax.set_title("Churn Rate by Tenure Group")

st.pyplot(fig)
st.subheader("Active vs Inactive Customer Churn")

activity_churn = filtered_df.groupby('IsActiveMember')['Exited'].mean()*100

fig, ax = plt.subplots(figsize=(6,4))
activity_churn.plot(kind='bar', ax=ax)

ax.set_xticklabels(['Inactive', 'Active'])
ax.set_ylabel("Churn Rate (%)")
ax.set_title("Churn Rate by Activity Status")

st.pyplot(fig)
st.subheader("Key Insights")

st.write("""
• Overall churn rate is 20.37%.

• Germany has the highest churn rate among all countries.

• Customers aged 46+ show higher churn behavior.

• High-balance customers contribute significantly to churn risk.

• Inactive customers are more likely to churn than active customers.

• Long-tenure customers show better retention.
""")