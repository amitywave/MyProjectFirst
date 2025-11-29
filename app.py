import streamlit as st
import plotly.express as px
from backend.database import init_db, add_stock, get_watchlist, remove_stock, get_stock_data

# 1. Initialize Database on startup
init_db()

# 2. Page Setup
st.set_page_config(page_title="Stock Watchlist", layout="wide")
st.title("📈 My Personal Stock Watchlist")

# --- SIDEBAR: Manage Watchlist ---
st.sidebar.header("Manage Favorites")
new_symbol = st.sidebar.text_input("Add Stock Symbol (e.g., AAPL, NVDA, RELIANCE.NS)")

if st.sidebar.button("Add to Watchlist"):
    if new_symbol:
        msg = add_stock(new_symbol)
        st.sidebar.success(msg)

# Show current watchlist in sidebar
st.sidebar.subheader("Your Watchlist")
watchlist = get_watchlist()
selected_stock = st.sidebar.radio("Select a stock to view:", watchlist)

if st.sidebar.button("Remove Selected Stock"):
    if selected_stock:
        remove_stock(selected_stock)
        st.rerun() # Refresh the app

# --- MAIN PAGE: Charts & Data ---
if selected_stock:
    st.subheader(f"Analysis: {selected_stock}")
    
    # Call Backend to get data
    with st.spinner("Fetching data..."):
        df = get_stock_data(selected_stock)
    
    if not df.empty:
        # Show Price Chart
        fig = px.line(df, y='Close', title=f'{selected_stock} Price Trend')
        st.plotly_chart(fig, use_container_width=True)
        
        # Show Data Table
        with st.expander("View Raw Data"):
            st.dataframe(df)
    else:
        st.error("Could not fetch data. Check the symbol.")
else:
    st.info("Your watchlist is empty! Add a stock in the sidebar to get started.")