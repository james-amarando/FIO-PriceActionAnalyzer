import yfinance as yf


def getPriceData(ticker, num_days=10):
    period = str(num_days) + "d"
    priceData = yf.download(tickers=ticker, period=period, interval="1d")
    return priceData


if __name__ == "__main__":
    ticker = "ACN"
    print("Testing API...")
    print("Using ticker: "+ticker)
    priceData = getPriceData(ticker=ticker, num_days=20)
    print("Got data:")
    print(priceData)
    print("\n\n\n")
    print("===================")
    print(" ARRAY INDEX CHECK")
    print("====================")
    print("\n\n")
    print("Price close:")
    print(priceData["Close"])
    print("\n\n")
    print("Most recent closing price:")
    print(priceData["Close"][-1:])
    print("\n\n")
    print("Last 5 most recent closing prices:")
    print(priceData["Close"][-5:])
    print("\n\n\n")
    print("===================")
    print(" DATA INDEX CHECK")
    print("====================")
    print("Most recent closing price - raw data only:")
    last_price = float(priceData["Close"][-1:])
    print(last_price)