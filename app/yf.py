import yfinance as yf
import streamlit as st
import plotly.graph_objs as go

# Function to fetch the latest stock price
@st.cache_data(ttl=30)  # Cache the function so it only updates every 30 seconds
def get_latest_price(ticker):
    data = yf.download(tickers=ticker, period="1d", interval="1m")
    if not data.empty:
        return data['Close'].iloc[-1]
    else:
        return None

# Initialize the app
st.title('Live Stock Data from Yahoo Finance')

# Input fields for user input
ticker = st.text_input('Enter the stock ticker symbol (e.g. AAPL):')
period = st.selectbox('Select the period:', ('1d', '7d', '1mo', '3mo', '6mo', '1y', '10y', 'ytd', 'max'))
interval = st.selectbox('Select the interval:', ('1h', '1d', '5d', '1wk', '1mo', '3mo'))

# Placeholder for live price counter
live_price_placeholder = st.empty()

# Fetch data button
if st.button('Fetch Data') or ticker:
    # Show live price
    latest_price = get_latest_price(ticker)
    if latest_price is not None:
        live_price_placeholder.metric(label=f"Latest price of {ticker}", value=f"USD {latest_price:.2f}")
    else:
        live_price_placeholder.error(f"Could not retrieve the price for {ticker}. Try again later.")

    # Fetch and display historical data
    with st.spinner('Fetching historical/Live data...'):
        historical_data = yf.download(tickers=ticker, period=period, interval=interval)
        st.write(f"Displaying {interval} candlestick chart for {ticker}")

        # Check if historical data is not empty
        if not historical_data.empty:
            # Candlestick chart
            fig = go.Figure(data=[go.Candlestick(x=historical_data.index,
                                                 open=historical_data['Open'],
                                                 high=historical_data['High'],
                                                 low=historical_data['Low'],
                                                 close=historical_data['Close'])])
            fig.update_layout(title=f'Candlestick chart for {ticker}',
                              yaxis_title='Stock Price')

            # Display candlestick chart
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error(f"Could not retrieve selected time range for {ticker}. Please adjust")

