import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_ta as ta  # NEW: For technical analysis
from streamlit_option_menu import option_menu # NEW: For cool menu
import plotly.express as px

# --- BACKEND FUNCTIONS (Keep these here or in backend/database.py) ---
def get_stock_data(symbol):
    # Fetch 6 months of data
    df = yf.Ticker(symbol).history(period="6mo")
    return df

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Pro Stock Dashboard", layout="wide")

# --- SIDEBAR: NEW NAVIGATION MENU ---
with st.sidebar:
    selected = option_menu("Main Menu", ["Dashboard", "Learn", "Settings"], 
        icons=['graph-up-arrow', 'book', 'gear'], menu_icon="cast", default_index=0)
    
    st.write("---")
    st.header("Stock Selector")
    country = st.radio("Market", ["India (NSE)", "USA"])
    user_input = st.text_input("Symbol", "RELIANCE")

    if country == "India (NSE)" and not user_input.endswith(".NS"):
        user_input = f"{user_input}.NS"

# --- MAIN PAGE LOGIC ---
if selected == "Dashboard":
    st.title(f"📊 Analysis: {user_input}")

    # 1. Fetch Data
    df = get_stock_data(user_input)

    if not df.empty:
        # 2. Add Indicators (The Magic of pandas_ta)
        df.ta.rsi(length=14, append=True)  # Adds an 'RSI_14' column automatically!
        
        # 3. Create Tabs for better organization
        tab1, tab2 = st.tabs(["Price Chart", "RSI Indicator"])

        with tab1:
            st.subheader("Price Movement")
            st.line_chart(df["Close"])
        
        with tab2:
            st.subheader("Relative Strength Index (RSI)")
            # Plot RSI with a red line at 70 (Overbought) and green at 30 (Oversold)
            st.line_chart(df["RSI_14"])
            st.caption("RSI > 70 = Overbought (Sell?), RSI < 30 = Oversold (Buy?)")
    
    else:
        st.error("No data found. Check the symbol.")

elif selected == "Learn":
    st.title("📚 Learning Center")
    st.write("Here you can add definitions of RSI, MACD, etc.")