import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Set page configuration
st.set_page_config(page_title="Economic Data Analysis Dashboard", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .main { background-color: #f5f7fa; }
    .sidebar .sidebar-content { background-color: #e1e8f0; }
    .stButton>button { background-color: #4e73df; color: white; border-radius: 5px; }
    .stSelectbox, .stSlider { background-color: white; border-radius: 5px; padding: 10px; }
    h1, h2, h3 { color: #2e3b55; }
    .metric-card { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

# Load dataset
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("salesforcourse-4fe2kehu.csv")  # Update path if necessary
        # Data cleaning
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Year_Month'] = df['Year'].astype(str) + '-' + df['Month']
        df['profit'] = df['Revenue'] - df['Cost']
        return df
    except FileNotFoundError:
        st.error("Error: The file 'salesforcourse-4fe2kehu.csv' was not found. Please ensure the file is in the correct directory or provide the correct path.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"An error occurred while loading the data: {str(e)}")
        return pd.DataFrame()

df = load_data()

# Stop execution if data loading failed
if df.empty:
    st.stop()

# Sidebar for filters
st.sidebar.header("Filters")
country = st.sidebar.selectbox("Select Country", ["All"] + sorted(df["Country"].unique().tolist()))
year = st.sidebar.selectbox("Select Year", ["All"] + sorted(df["Year"].unique().astype(int).tolist()))
product_category = st.sidebar.selectbox("Select Product Category", ["All"] + sorted(df["Product Category"].unique().tolist()))
age_range = st.sidebar.slider("Customer Age Range", int(df["Customer Age"].min()), int(df["Customer Age"].max()), (int(df["Customer Age"].min()), int(df["Customer Age"].max())))

# Apply filters
filtered_df = df.copy()
if country != "All":
    filtered_df = filtered_df[filtered_df["Country"] == country]
if year != "All":
    filtered_df = filtered_df[filtered_df["Year"] == year]
if product_category != "All":
    filtered_df = filtered_df[filtered_df["Product Category"] == product_category]
filtered_df = filtered_df[(filtered_df["Customer Age"] >= age_range[0]) & (filtered_df["Customer Age"] <= age_range[1])]

# Main title
st.title("Economic Data Analysis Dashboard")
st.markdown("Interactive dashboard for analyzing sales transactions (2015-2016).")

# Summary Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("Total Revenue")
    st.markdown(f"${filtered_df['Revenue'].sum():,.2f}")
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("Total Profit")
    st.markdown(f"${filtered_df['profit'].sum():,.2f}")
    st.markdown('</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("Total Quantity Sold")
    st.markdown(f"{filtered_df['Quantity'].sum():,.0f}")
    st.markdown('</div>', unsafe_allow_html=True)

# Monthly Performance Line Chart
st.subheader("Monthly Revenue, Cost, and Profit Trends")
grouped = filtered_df.groupby(['Year_Month'])[['Cost', 'Revenue', 'profit']].sum().reset_index()
fig1 = px.line(grouped, x='Year_Month', y=['Cost', 'Revenue', 'profit'], title='Monthly Performance',
               labels={'value': 'Amount ($)', 'variable': 'Metric'})
fig1.update_layout(title_x=0.5, height=500)
st.plotly_chart(fig1, use_container_width=True)

# Two-column layout for additional charts
col_left, col_right = st.columns(2)

with col_left:
    # Top Selling Sub-Categories by Quantity
    st.subheader("Top Selling Sub-Categories by Quantity")
    category_sales = filtered_df.groupby('Sub Category')['Quantity'].sum().reset_index().sort_values('Quantity', ascending=False)
    fig2 = px.bar(category_sales, y='Sub Category', x='Quantity', text_auto='.2s',
                  title="Product Sales Quantity by Sub Category",
                  labels={'Quantity': 'Quantity Sold'})
    fig2.update_layout(title_x=0.5, height=500)
    st.plotly_chart(fig2, use_container_width=True)

    # Profit by Country Pie Chart
    st.subheader("Profit Distribution by Country")
    country_profit = filtered_df.groupby('Country')['profit'].sum().reset_index()
    fig4 = px.pie(country_profit, values='profit', names='Country', title="Profit by Country",
                  color_discrete_sequence=px.colors.sequential.RdBu)
    fig4.update_layout(title_x=0.5, height=400)
    st.plotly_chart(fig4, use_container_width=True)

with col_right:
    # Top Selling Sub-Categories by Profit
    st.subheader("Top Sub-Categories by Profit")
    category_profit = filtered_df.groupby('Sub Category')['profit'].sum().reset_index().sort_values('profit', ascending=False)
    fig3 = px.bar(category_profit, y='Sub Category', x='profit', text_auto='.2s',
                  title="Profit by Sub Category",
                  labels={'profit': 'Profit ($)'})
    fig3.update_layout(title_x=0.5, height=500)
    st.plotly_chart(fig3, use_container_width=True)

    # Top Selling Products by Customer Age
    st.subheader("Top Selling Products by Customer Age")
    df_grouped = filtered_df.groupby(['Customer Age', 'Sub Category'])['Quantity'].sum().reset_index()
    top_products = df_grouped.groupby('Customer Age').apply(lambda x: x.loc[x['Quantity'].idxmax()]).reset_index(drop=True)
    fig5 = px.bar(top_products, x='Customer Age', y='Quantity', color='Sub Category',
                  title="Top Selling Sub-Category by Customer Age")
    fig5.update_layout(title_x=0.5, height=400)
    st.plotly_chart(fig5, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Developed for Economic Data Analysis Project | Data Source: salesforcourse-4fe2kehu.csv")
