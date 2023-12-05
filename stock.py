import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

def get_stock_data(tickers, start_date, end_date):
    data = {}
    for ticker in tickers:
        data[ticker] = yf.download(ticker, start=start_date, end=end_date)
    return data

def main():
    st.title('Stock Price Visualizer')

    # User input (excluding Burger King)
    tickers = st.text_input('Enter stock ticker symbols (e.g., AAPL, TSLA, MCD, GOOGL, AMZN, DELL):', 'AAPL,TSLA,MCD,GOOGL,AMZN,DELL').split(',')
    start_date = st.date_input('Select start date:', pd.to_datetime('2022-01-01'))
    end_date = st.date_input('Select end date:', pd.to_datetime('2023-01-01'))

    # Fetch stock data
    stock_data = get_stock_data(tickers, start_date, end_date)

    # Display raw stock data
    st.subheader('Raw Stock Data')
    for ticker, data in stock_data.items():
        st.write(f'{ticker} Stock Data')
        st.write(data)

    # Plot closing price for each stock
    for ticker, data in stock_data.items():
        fig = px.line(data, x=data.index, y='Close', title=f'{ticker} Stock Price')
        fig.update_xaxes(title_text='Date')
        fig.update_yaxes(title_text='Closing Price (USD)')
        st.plotly_chart(fig)

    # Additional analysis (e.g., moving average) for each stock
    st.subheader('Additional Analysis')

    for ticker, data in stock_data.items():
        sma_period = st.slider(f'Select SMA period for {ticker}:', min_value=1, max_value=100, value=20)
        data['SMA'] = data['Close'].rolling(window=sma_period).mean()

        # Plot SMA
        fig_sma = px.line(data, x=data.index, y=['Close', 'SMA'],
                          title=f'{ticker} Stock Price with {sma_period}-Day SMA')
        fig_sma.update_xaxes(title_text='Date')
        fig_sma.update_yaxes(title_text='Price (USD)')
        st.plotly_chart(fig_sma)

if __name__ == "__main__":
    # Set default values for stocks
    st.set_page_config(page_title='Stock Price Visualizer', page_icon=':chart_with_upwards_trend:')
    main()
