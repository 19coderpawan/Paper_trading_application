import yfinance as yf
import requests

# instead of manually maintaing the mapping we can always fetch it ,we can totally make \
# this dynamic so you don’t have to maintain NAME_TO_TICKER manually.

def fetch_ticker_mapping():
    mapping={}
    #For stocks: Use the free NASDAQ Symbol Directory  API to map company name → ticker.
    try:
        nasdaq_url="https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=5000"
        headers = {"User-Agent": "Mozilla/5.0"} # NASDAQ requires a User-Agent
        response=requests.get(nasdaq_url,headers)
        data=response.json()["data"]["rows"]
        for stock in data:
            symbol=stock["symbol"].strip().upper()
            name=stock["name"].strip().upper()
            mapping[name]=symbol
            mapping[symbol]=symbol  # also map ticker to itself

    except Exception as e:
        print(f"error fetching the data from nasdaq-: {e}")

    # For crypto: Use CoinGecko’s /coins/list API to map crypto name → symbol.    
    try:
        coin_url="https://api.coingecko.com/api/v3/coins/list"
        response=requests.get(coin_url)
        data=response.json()
        for crypto in data:
            symbol=crypto["symbol"].strip().upper()
            name=crypto["name"].strip().upper()
            mapping[name]=symbol
            mapping[symbol]=symbol
    except Exception as e:
        print(f"error fetching the data from coingecko-: {e}")    

    return mapping

NAME_TO_TICKER=fetch_ticker_mapping()    
            
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
    """Normalize user input to a valid ticker or crypto ID."""
    cleaned = user_input.strip().upper()
    return NAME_TO_TICKER.get(cleaned, cleaned) #if found symbol then return it else return cleaned.

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
    symbol=normalize_symbol(userInput)

    # Try as stock first
    price=get_stock_prices(symbol)
    if price is not None:
        return price,"stock"
    
    # Try crypto (first using symbol as-is, then try mapping common tickers to ids)
    crypto_price=get_crypto_prices(symbol)
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

