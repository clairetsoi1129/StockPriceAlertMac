##Pre-requisite##
pip3 install pandas-datareader, pync, yfinance

pip3 install pandas, alpha_vantage

##To use ssl to send email, please run below command in terminal##
open /Applications/Python\ 3.9/Install\ Certificates.command

##How to run##
python3 alphav_email_notify.py 

# Stock Price Alert

This project was created with Python version 3.9 using yahoo finance API and alpha vantage API.

1. It will trigger email alert or mac notification when stock price reach the target price.

## Pre-requisite

1. Install the below package by following commands

pip3 install pandas, pync

2. Install the below package to run yfin_price_notify by following commands

pip3 install pandas-datareader, yfinance

3. Install the below package to run alphav_price_notify by following commands

pip3 install alpha_vantage

4. Update the config_incomplete.py and rename it to config.py

5. To send email with SMTP over SSL, you may need to install SSL Certificate by following commands
open /Applications/Python\ 3.9/Install\ Certificates.command

## How to run the program

1. To trigger alpha vantage version, run the below
python3 alphav_price_notify.py 

2. To trigger yahoo finance version, run the below
python3 yfin_price_notify.py 

## Further help

