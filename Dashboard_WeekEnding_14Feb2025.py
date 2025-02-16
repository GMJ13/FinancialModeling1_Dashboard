import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Set page configuration
st.set_page_config(page_title="Portfolio Dashboard", layout="wide")


def load_data():
    """Load data from Excel file"""
    df = pd.read_excel('Group-6 Portfolio Dashboard_Week3_07022025.xlsx',
                       sheet_name=['Dashboard', 'Transactions', 'Charting'])
    return df


def format_currency(value):
    """Format numbers as currency"""
    return f"${value:,.2f}"


def create_dashboard():
    # Load data
    data = load_data()

    # Header
    st.title("Portfolio Dashboard")
    st.markdown("---")

    # Key Metrics Row
    col1, col2, col3 = st.columns(3)

    portfolio_value = 985158.59  # From the Excel data
    weekly_change = -13650.98
    total_gain_loss = -12869.64

    with col1:
        st.metric("Portfolio Value",
                  format_currency(portfolio_value),
                  format_currency(weekly_change))

    with col2:
        st.metric("Weekly Change",
                  format_currency(weekly_change),
                  format_currency(weekly_change))

    with col3:
        st.metric("Total Gain/Loss",
                  format_currency(total_gain_loss),
                  format_currency(total_gain_loss))

    st.markdown("---")

    # Portfolio Composition
    if 'Transactions' in data:
        transactions_df = data['Transactions']
        transactions_df.columns = transactions_df.loc[0]
        transactions_df = transactions_df.loc[1:]
        transactions_df = transactions_df.drop(transactions_df.columns[0], axis=1)
        transactions_df['Date'] = pd.to_datetime(transactions_df['Date'])

        # Group by asset type and calculate total value
        portfolio_composition = transactions_df.groupby('Asset')['Entry Price'].sum()

        # Create pie chart
        fig_composition = px.pie(
            values=portfolio_composition.values,
            names=portfolio_composition.index,
            title="Portfolio Composition by Asset Type"
        )
        st.plotly_chart(fig_composition)

    # Transaction History
    if 'Transactions' in data:
        st.subheader("Recent Transactions")
        st.dataframe(
            transactions_df.sort_values('Date', ascending=False)
            .head(10)
            [['Date', 'Asset', 'Ticker', 'Units', 'Entry Price']]
        )


if __name__ == "__main__":
    create_dashboard()