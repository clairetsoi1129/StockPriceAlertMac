import time
import pandas as pd #data manipulation and analysis package

from config import password, sender_email, rec_email, mac_notification, email_notification
from lib.util.mail_func import send_email_ssl_price_alert
from lib.util.mac_notification import price_notification

import yfinance as yf
from pandas_datareader import data as pdr
yf.pdr_override()

#Getting watchlist.csv and target price
watchlistDf = pd.read_csv('data/yfin_watchlist.csv')

while True:
    #Loop through the watchlist dataframe for ticker and check the price in yahoo finance
    for row in watchlistDf.itertuples(index=True, name='Pandas'):
        print(row.Ticker, row.AlertPrice)

        #Getting the data from yfinance
        #We are currently interested in the latest price
        last_price = pdr.get_data_yahoo(row.Ticker)["Close"][-1]
        print(last_price) 

        if row.last_price > row.AlertPrice:
            if email_notification:
                send_email_ssl_price_alert(sender_email, password, rec_email, row.Ticker, row.AlertPrice)
            if mac_notification: 
                price_notification(row.Ticker, row.AlertPrice)
            watchlistDf.at[row.Index,'EmailSent']=True

    # sleep 60sec
    time.sleep(60)