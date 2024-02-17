import streamlit as st
import pandas as pd
import os
import requests
import plotly.express as px

# Function to fetch price data from CoinGecko API
def fetch_price(ticker):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ticker}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()

    try:
        price = data[ticker]['usd']
        return price
    except KeyError:
        st.error(f"Error: Unable to fetch price for {ticker}. Please check the ticker symbol.")
        return None
    except Exception as e:
        st.error(f"Error occurred: {e}")
        return None

# Function to add entry to portfolio CSV
def add_entry_to_csv(ticker, amount, price, usd_value):
    filename = "portfolio.csv"
    if os.path.exists(filename):
        df = pd.read_csv(filename)
    else:
        df = pd.DataFrame(columns=['ticker', 'amount', 'price', 'usd_value'])

    new_entry = pd.DataFrame({'ticker': [ticker], 'amount': [amount], 'price': [price], 'usd_value': [usd_value]})
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(filename, index=False)

# Function to delete entry from portfolio CSV
def delete_entry_from_csv(index):
    filename = "portfolio.csv"
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        df = df.drop(index=index)
        df.to_csv(filename, index=False)
    st.rerun()

# Function to load portfolio data from CSV
def load_portfolio_from_csv():
    filename = "portfolio.csv"
    if os.path.exists(filename):
        df = pd.read_csv(filename)
    else:
        df = pd.DataFrame(columns=['ticker', 'amount', 'price', 'usd_value'])
    return df

# Streamlit App
def main():
    st.title('Crypto Portfolio App')

    # Sidebar for user input
    with st.sidebar:
        st.subheader('Add Entry')
        ticker = st.text_input('Enter Ticker Symbol')
        amount = st.number_input('Enter Amount')

        if st.button('Add to Portfolio'):
            price = fetch_price(ticker)
            if price is not None:
                usd_value = amount * price
                add_entry_to_csv(ticker, amount, price, usd_value)

    # Display portfolio overview and delete entry section side by side
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader('Portfolio Overview')
        df = load_portfolio_from_csv()
        if not df.empty:
            total_usd_value = df['usd_value'].sum()
            df['percentage'] = df['usd_value'] / total_usd_value * 100
            st.write(df)

            # Add space between portfolio overview and pie chart
            st.write("")
            st.write("")

            # Plot percentage of USD value for each coin
            fig = px.pie(df, values='usd_value', names='ticker', title='Portfolio Allocation')
            st.plotly_chart(fig)
        else:
            st.write('No entries added yet.')

    with col2:
        st.subheader('Delete Entry')
        delete_index = st.selectbox('Select entry to delete', options=df.index, help='Select the row number to delete')
        if st.button('Delete'):
            delete_entry_from_csv(delete_index)

if __name__ == "__main__":
    main()

