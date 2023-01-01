import os
import pync

def price_notification(ticker, price):
    pync.notify(group=os.getpid(),
                        title=f"Price Alert for {ticker}",
                        message=f"{ticker} has reached a price of {price}:.2f",
                        open=f"http://finance.yahoo.com/q?s={ticker}")