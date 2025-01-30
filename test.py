from kite_trade import *
import pandas as pd 
import datetime
import os
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
user_id = config['zerodha']['userID']
enctoken = get_enctoken(user_id, config['zerodha']['password'])
kite = KiteApp(enctoken=enctoken)
datetime_now = datetime.datetime.now()

# print(kite.margins())
# print(kite.orders())
# print(kite.positions())

import requests
instruments_fileName = f"./data/instruments_{datetime_now.strftime('%d-%m-%Y')}.csv"
# download the instruments file from the kite api and save it to the data folder with today's date
if not os.path.exists(instruments_fileName):
    instruments = requests.get("https://api.kite.trade/instruments", headers={"Authorization": f"enctoken {enctoken}"}).text
    with open(instruments_fileName, "w") as f:
        f.write(instruments)
# search for a particular instument based on tradingsymbol, segment=CDS-FUT and print results
json_instruments = pd.read_csv(f"./data/instruments_{datetime_now.strftime('%d-%m-%Y')}.csv")

instrument_token = json_instruments[(json_instruments['tradingsymbol'] == 'USDINR25FEBFUT') & (json_instruments['segment'] == 'CDS-FUT')]['instrument_token'].values[0]
instrument_storagePath = f'./data/{instrument_token}'
instrument_storagePath_postfix = f'/{datetime_now.strftime("%d-%m-%Y#%H-%M")}.csv'
# print(kite.quote(instrument_token))
# print(kite.ltp("NSE:RELIANCE"))
# print(kite.ltp(instrument_token))
from_datetime = datetime_now - datetime.timedelta(days=10)     # From last & days
to_datetime = datetime.datetime.now()
interval = kite.INTERVAL_1M
df = pd.DataFrame(kite.historical_data(instrument_token, from_datetime, to_datetime, interval, continuous=False, oi=False, user = user_id), index=None)
if(os.path.exists(instrument_storagePath) and os.path.isdir(instrument_storagePath)):
    df.to_csv(instrument_storagePath + instrument_storagePath_postfix)
else:
    os.makedirs(instrument_storagePath)
    df.to_csv(instrument_storagePath + instrument_storagePath_postfix)

# Place Order
# order = kite.place_order(variety=kite.VARIETY_REGULAR,
#                          exchange=kite.EXCHANGE_NSE,
#                          tradingsymbol="ACC",
#                          transaction_type=kite.TRANSACTION_TYPE_BUY,
#                          quantity=1,
#                          product=kite.PRODUCT_MIS,
#                          order_type=kite.ORDER_TYPE_MARKET,
#                          price=None,
#                          validity=None,
#                          disclosed_quantity=None,
#                          trigger_price=None,
#                          squareoff=None,
#                          stoploss=None,
#                          trailing_stoploss=None,
#                          user=user_id,
#                          tag="RadiiHoldings")
