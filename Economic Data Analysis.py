import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Set page configuration
st.set_page_config(page_title="Cost of Living Analysis Dashboard", layout="wide")

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
        df = pd.read_csv("Cost_of_Living_Index_2022.csv")
        return df
    except FileNotFoundError:
        st.error("Error: The file 'Cost_of_Living_Index_2022.csv' was not found. Please ensure the file is in the correct directory or provide the correct path.")
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

# Apply filters
filtered_df = df.copy()
if country != "All":
    filtered_df = filtered_df[filtered_df["Country"] == country]

# Main title
st.title("Cost of Living Analysis Dashboard")
st.markdown("Interactive dashboard for analyzing cost-of-living indices across countries (2022).")

# Summary Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("Average Cost of Living Index")
    st.markdown(f"{filtered_df['Cost of Living Index'].mean():,.2f}")
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("Average Rent Index")
    st.markdown(f"{filtered_df['Rent Index'].mean():,.2f}")
    st.markdown('</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("Average Purchasing Power Index")
    st.markdown(f"{filtered_df['Local Purchasing Power Index'].mean():,.2f}")
    st.markdown('</div>', unsafe_allow_html=True)

# Cost of Living vs. Rent Index Scatter Plot
st.subheader("Cost of Living vs. Rent Index by Country")
fig1 = px.scatter(filtered_df, x='Cost of Living Index', y='Rent Index', color='Country',
                  size='Local Purchasing Power Index', hover_data=['Country'],
                  title='Cost of Living vs. Rent Index (Size: Purchasing Power)',
                  labels={'Cost of Living Index': 'Cost of Living Index', 'Rent Index': 'Rent Index'})
fig1.update_layout(title_x=0.5, height=500, showlegend=False if country != "All" else True)
st.plotly_chart(fig1, use_container_width=True)

# Two-column layout for additional charts
col_left, col_right = st.columns(2)

with col_left:
    # Top Countries by Cost of Living Index
    st.subheader("Top Countries by Cost of Living Index")
    top_cost = filtered_df[['Country', 'Cost of Living Index']].sort_values('Cost of Living Index', ascending=False).head(10)
    fig2 = px.bar(top_cost, x='Cost of Living Index', y='Country', text_auto='.2f',
                  title="Top 10 Countries by Cost of Living Index",
                  labels={'Cost of Living Index': 'Cost of Living Index'})
    fig2.update_layout(title_x=0.5, height=400)
    st.plotly_chart(fig2, use_container_width=True)

    # Groceries Index Distribution
    st.subheader("Groceries Index Distribution")
    fig4 = px.histogram(filtered_df, x='Groceries Index', nbins=20,
                        title="Distribution of Groceries Index Across Countries",
                        labels={'Groceries Index': 'Groceries Index'})
    fig4.update_layout(title_x=0.5, height=400)
    st.plotly_chart(fig4, use_container_width=True)

with col_right:
    # Top Countries by Purchasing Power Index
    st.subheader("Top Countries by Purchasing Power Index")
    top_purchasing = filtered_df[['Country', 'Local Purchasing Power Index']].sort_values('Local Purchasing Power Index', ascending=False).head(10)
    fig3 = px.bar(top_purchasing, x='Local Purchasing Power Index', y='Country', text_auto='.2f',
                  title="Top 10 Countries by Purchasing Power Index",
                  labels={'Local Purchasing Power Index': 'Purchasing Power Index'})
    fig3.update_layout(title_x=0.5, height=400)
    st.plotly_chart(fig3, use_container_width=True)

    # Restaurant Price Index vs. Purchasing Power
    st.subheader("Restaurant Price vs. Purchasing Power")
    fig5 = px.scatter(filtered_df, x='Restaurant Price Index', y='Local Purchasing Power Index',
                      color='Country', hover_data=['Country'],
                      title="Restaurant Price Index vs. Purchasing Power Index",
                      labels={'Restaurant Price Index': 'Restaurant Price Index', 'Local Purchasing Power Index': 'Purchasing Power Index'})
    fig5.update_layout(title_x=0.5, height=400, showlegend=False if country != "All" else True)
    st.plotly_chart(fig5, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Developed for Cost of Living Analysis Project | Data Source: Cost_of_Living_Index_2022.csv")
