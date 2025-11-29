import sqlite3
import yfinance as yf

# --- DATABASE MANAGEMENT ---
def init_db():
    """Create the database and table if they don't exist."""
    conn = sqlite3.connect('stocks.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS watchlist (symbol TEXT PRIMARY KEY)')
    conn.commit()
    conn.close()

def add_stock(symbol):
    """Add a stock symbol to the database."""
    try:
        conn = sqlite3.connect('stocks.db')
        c = conn.cursor()
        c.execute('INSERT INTO watchlist (symbol) VALUES (?)', (symbol.upper(),))
        conn.commit()
        conn.close()
        return f"Added {symbol} to watchlist!"
    except sqlite3.IntegrityError:
        return f"{symbol} is already in your watchlist."

def get_watchlist():
    """Retrieve all saved stocks."""
    conn = sqlite3.connect('stocks.db')
    c = conn.cursor()
    c.execute('SELECT symbol FROM watchlist')
    data = c.fetchall()
    conn.close()
    return [row[0] for row in data]

def remove_stock(symbol):
    """Remove a stock from the database."""
    conn = sqlite3.connect('stocks.db')
    c = conn.cursor()
    c.execute('DELETE FROM watchlist WHERE symbol = ?', (symbol,))
    conn.commit()
    conn.close()

# --- DATA FETCHING (YFINANCE) ---
def get_stock_data(symbol):
    """Fetch history for a stock."""
    stock = yf.Ticker(symbol)
    df = stock.history(period="1y") # Get 1 year of data
    return df