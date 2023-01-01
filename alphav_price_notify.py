import time
import pandas as pd #data manipulation and analysis package

from config import password, sender_email, rec_email, mac_notification, email_notification
from lib.util.mail_func import send_email_ssl_price_alert
from lib.util.mac_notification import price_notification

from config import alphav_api_key
from alpha_vantage.timeseries import TimeSeries #enables data pull from Alpha Vantage

#Getting watchlist.csv and target price
watchlistDf = pd.read_csv('data/alphav_watchlist.csv')
watchlistDf["EmailSent"] = watchlistDf["EmailSent"].astype(bool)

#Getting the data from alpha_vantage
ts = TimeSeries(key=alphav_api_key, output_format='pandas')

while True:
    for row in watchlistDf.itertuples(index=True, name='Pandas'):
        print(row.Ticker, row.AlertPrice, row.EmailSent)
        if row.EmailSent == False:
            data, meta_data = ts.get_intraday(row.Ticker,interval='1min', outputsize='full')

            #We are currently interested in the latest price
            close_data = data['4. close'] #The close data column
            last_price = close_data[0] #Selecting the last price from the close_data column
            #Check if you're getting a correct value
            print(last_price) 

            if last_price > row.AlertPrice:
                if email_notification:
                    send_email_ssl_price_alert(sender_email, password, rec_email, row.Ticker, row.AlertPrice)
                if mac_notification: 
                    price_notification(row.Ticker, row.AlertPrice)
            watchlistDf.at[row.Index,'EmailSent']=True
        
        # sleep 60sec
        time.sleep(60)