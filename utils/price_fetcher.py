import yfinance as yf
import requests
import threading

# Global cache for name-to-ticker mapping
NAME_TO_TICKER = {}
MAPPINGS_READY = False

# instead of manually maintaing the mapping we can always fetch it ,we can totally make \
# this dynamic so you don’t have to maintain NAME_TO_TICKER manually.

def fetch_symbol_mappings():
    """Fetch mappings from NASDAQ + CoinGecko in background."""
    global NAME_TO_TICKER, MAPPINGS_READY
    try:
        local_map = {}

        # --- Fetch stock list from NASDAQ ---
        nasdaq_url = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=5000"
        headers = {"User-Agent": "Mozilla/5.0"}
        stocks = requests.get(nasdaq_url, headers=headers, timeout=15).json()
        for row in stocks.get("data", {}).get("rows", []):
            local_map[row["name"].upper()] = row["symbol"]

        # --- Fetch crypto list from CoinGecko ---
        cryptos = requests.get("https://api.coingecko.com/api/v3/coins/list", timeout=15).json()
        for c in cryptos:
            local_map[c["name"].upper()] = c["symbol"].upper()
            local_map[c["symbol"].upper()] = c["symbol"].upper()

        NAME_TO_TICKER = local_map
        MAPPINGS_READY = True
        print(f"[INFO] Background: Loaded {len(NAME_TO_TICKER)} mappings ✅")

    except Exception as e:
        print(f"[ERROR] Background mapping fetch failed: {e}")


# --- Start background fetch at import ---
threading.Thread(target=fetch_symbol_mappings, daemon=True).start()

            
#A name-to-ticker mapping for stocks and cryptos.
# so that user can type company name like apple instead of appl for better expericence.
# NAME_TO_TICKER = {
#     # Stocks
#     "APPLE": "AAPL",
#     "GOOGLE": "GOOGL",
#     "TESLA": "TSLA",
#     "MICROSOFT": "MSFT",
#     "AMAZON": "AMZN",
#     "META": "META",
#     "NETFLIX": "NFLX",

#     # Cryptos
#     "BITCOIN": "bitcoin",
#     "ETHEREUM": "ethereum",
#     "DOGECOIN": "dogecoin",
#     "CARDANO": "cardano"
# }

def normalize_symbol(user_input: str) -> str:
    """Normalize user input to ticker if mapping is ready."""
    cleaned = user_input.strip().upper()
    if MAPPINGS_READY:
        return NAME_TO_TICKER.get(cleaned, cleaned)
    return cleaned  # fallback until mappings are ready


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

def get_prices(userInput)->tuple:
    '''Unified price fetcher. Returns (price, market_type).
    Automatically detects if it's a stock or crypto.'''
     
    
    # normalizing the user input to ticker symbol.
    # symbol=normalize_symbol(userInput)

    # Try as stock first
    price=get_stock_prices(userInput)
    if price is not None:
        return price,"stock"
    
    # Try crypto (first using symbol as-is, then try mapping common tickers to ids)
    crypto_price=get_crypto_prices(userInput)
    if crypto_price is not None:
        return crypto_price,"crypto"
    
    # if not found , then try mapping the ticker to ids.
    # crypto_map={
    #     "BTC": "bitcoin",
    #     "ETH": "ethereum",
    #     "DOGE": "dogecoin",
    #     "ADA": "cardano"
    # }

    # if symbol.upper() in crypto_map:
    #     crypto_price=get_crypto_prices(crypto_map[symbol.upper()])
    #     if crypto_price is not None:
    #         return crypto_price,"crypto"

    return None,None    

