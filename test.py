from kite_trade import *
import pandas as pd 
import datetime
import os

user_id = 'HQ2948'
enctoken = "g/Q0/ePTzQozQmMe9CmBK0pvHIl8rxeLY8MFs4ybR4vOrQIQxK2f99QVVLW4Ckf9AUuKOLevDjZeexZv9oi82LCmVCzJR0uWJfBKT8IBvECVZKXGLRmHgA=="
kite = KiteApp(enctoken=enctoken)
datetime_now = datetime.datetime.now()

# print(kite.margins())
# print(kite.orders())
# print(kite.positions())

instrument_token = 2433027
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
