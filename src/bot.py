import degiroapi
import requests
import yfinance as yf
from degiroapi.product import Product
from degiroapi.order import Order
from degiroapi.utils import pretty_json
import credentials
import etfs


import pandas as pd
from datetime import datetime, timedelta

requests.get('http://charting.vwdservices.com', verify=False)



# start the session

degiro = degiroapi.DeGiro()
degiro.login(credentials.username, credentials.password)


# Log the session details
session = {}
cashfunds = degiro.getdata(degiroapi.Data.Type.CASHFUNDS)
portfolio = degiro.getdata(degiroapi.Data.Type.PORTFOLIO, True)


# Get the products from the ETFsx
for etf_name, tickr in etfs.list.items():
	product = yf.Ticker(tickr)
	data = yf.download(tickr, period = "2m")
	print(product.info['shortName'])
	print(product.history(period="max"))


#try:
#    products = degiro.search_products('spy')
#    realprice = degiro.real_time_price(Product(products[0]).id, degiroapi.Interval.Type.One_Day)
#except requests.exceptions.ConnectionError:
#    print("Connection refused")
# Interval can be set to One_Day, One_Week, One_Month, Three_Months, Six_Months, One_Year, Three_Years, Five_Years, Max
#realprice = degiro.real_time_price(Product(products[0]).id, degiroapi.Interval.Type.One_Day)

# getting the real time price
#print(realprice[0]['data']['lastPrice'])
#print(pretty_json(realprice[0]['data']))
#	realtime_price = degiro.real_time_price(product['id'], degiroapi.Interval.Type.One_Day)
#	df = pd.DataFrame(realtime_price[1]['data'])
#	print(df.head())

