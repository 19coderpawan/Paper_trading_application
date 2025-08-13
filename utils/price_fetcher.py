import yfinance as yf
import requests

def get_stock_prices(symbol)->float:
    # """Fetch latest stock price using Yahoo Finance."""
    try:
        ticker=yf.Ticker(symbol)
        data=ticker.history(period="1d") #one day data in dataframe form.
        if not data.empty:
            return float(data['Close'].iloc[-1])
    except Exception as e:
        print(f"Stock price fetch error for {symbol}: {e}")
    return None    


def get_crypto_prices(symbol)->float:
    """Fetch latest crypto price from CoinGecko."""

    try:
        # CoinGecko expects lowercase names like 'bitcoin', not 'BTC'
        url=f"https://api.coingecko.com/api/v3/simple/price?ids={symbol.lower()}&vs_currencies=usd"
        response=requests.get(url,timeout=5)
        data=response.json()
        if symbol.lower() in data:
            return float(data[symbol.lower()]['usd'])
    except Exception as e:
        print((f"Crypto price fetch error for {symbol}: {e}"))   
    return None     

def get_prices(symbol)->tuple:
    '''Unified price fetcher. Returns (price, market_type).
    Automatically detects if it's a stock or crypto.'''

    # Try as stock first
    price=get_stock_prices(symbol)
    if price is not None:
        return price,"stock"
    
    # Try crypto (first using symbol as-is, then try mapping common tickers to ids)
    crypto_price=get_crypto_prices(symbol)
    if crypto_price is not None:
        return crypto_price,"crypto"
    
    # if not found , then try mapping the ticker to ids.
    crypto_map={
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "DOGE": "dogecoin",
        "ADA": "cardano"
    }

    if symbol.upper() in crypto_map:
        crypto_price=get_crypto_prices(crypto_map[symbol.upper()])
        if crypto_price is not None:
            return crypto_price,"crypto"

    return None,None    

