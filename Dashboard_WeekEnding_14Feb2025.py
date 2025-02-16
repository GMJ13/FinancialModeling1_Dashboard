import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import yfinance as yf

# Set page configuration
st.set_page_config(page_title="Portfolio Dashboard", layout="wide")


def load_data():
    """Load data from Excel file"""
    df = pd.read_excel('Group-6 Portfolio Dashboard_Week3_07022025.xlsx',
                       sheet_name=['Dashboard', 'Transactions','Portfolio_Summary'])
    return df


def format_currency(value):
    """Format numbers as currency"""
    return f"${value:,.2f}"

def data_dashboardClean(dataClean):
    dataClean = dataClean.loc[5:].reset_index(drop=True)
    dataClean.columns = dataClean.loc[0]
    dataClean = dataClean.loc[1:].reset_index(drop=True)
    dataClean = dataClean.loc[dataClean.notna().any(axis=1)].round(decimals=2)
    dataClean = dataClean.drop(dataClean.columns[0], axis=1)
    dataClean['Gain (Loss)'] = dataClean['Gain (Loss)'].apply(lambda x: round(x, 2))
    dataClean = dataClean.fillna('-')

    for iterTick in range(1,len(dataClean)):
        dataClean['Asset'][iterTick] = yf.Ticker(dataClean['Ticker'][iterTick]).info['longName']

    #dataClean = dataClean.reset_index(range(1,len(dataClean)),drop=True)
    return dataClean


def create_dashboard():
    # Load data
    data = load_data()

    # Header
    st.title("Portfolio Dashboard")
    st.markdown("---")

    # Key Metrics Row
    col1, col2 = st.columns(2)

    prev_week_portfolioVal = data['Portfolio_Summary'].iloc[0,0].round(decimals=2)
    portfolio_value        = data['Portfolio_Summary'].iloc[0,1].round(decimals=2)  # From the Excel data
    prev_weekly_change = data['Portfolio_Summary'].iloc[0, 2].round(decimals=2)
    weekly_change          = data['Portfolio_Summary'].iloc[0,3].round(decimals=2)
    total_gain_loss        = data['Portfolio_Summary'].iloc[0,4].round(decimals=2)


    with col1:
        st.metric("Portfolio Value",
                  format_currency(portfolio_value),
                  (-abs(-prev_week_portfolioVal + portfolio_value)).round(decimals=2) if (-prev_week_portfolioVal + portfolio_value) < 0 else (
                    -prev_week_portfolioVal + portfolio_value).round(decimals=2))

        st.metric("Previous Week Portfolio Value",
                  format_currency(prev_week_portfolioVal))
    with col2:
        st.metric("Total Gain/Loss",
                  format_currency(total_gain_loss),
                  (-abs(total_gain_loss-prev_weekly_change)).round(decimals=2) if (total_gain_loss-prev_weekly_change) < 0 else (total_gain_loss-prev_weekly_change).round(decimals=2))

        st.metric("Previous Week Total Gain/Loss",
                  format_currency(prev_weekly_change))


    st.markdown("---")

    data['Dashboard'] = data_dashboardClean(data['Dashboard'])

    # Display Current Holdings
    st.subheader("Current Holdings Information")
    st.dataframe(
        data['Dashboard']
    )

    # Portfolio Composition
    if 'Transactions' in data:
        transactions_df = data['Transactions']
        transactions_df.columns = transactions_df.loc[0]
        transactions_df = transactions_df.loc[1:]
        transactions_df = transactions_df.drop(transactions_df.columns[0], axis=1)
        transactions_df['Date'] = pd.to_datetime(transactions_df['Date'])

        # Group by asset type and calculate total value
        portfolio_composition = transactions_df.groupby('Sector')['Entry Price'].sum()

        # Create pie chart
        fig_composition = px.pie(
            values=portfolio_composition.values,
            names=portfolio_composition.index,
            title="Portfolio Composition by Sector Type"
        )
        st.plotly_chart(fig_composition)

    # Transaction History
    if 'Transactions' in data:
        st.subheader("Recent Transactions")
        st.dataframe(
            transactions_df.sort_values('Date', ascending=False).set_index('Date',drop=True)
            [['Sector', 'Ticker','Transaction Type', 'Units', 'Entry Price','Transaction Amount','Transaction Cost','Total Transaction','Currency']]
        )


if __name__ == "__main__":
    create_dashboard()