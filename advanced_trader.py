import ourbit.ourbit_v3 as ourbit_spot_v3
import json
import datetime
import pandas as pd
import numpy as np
import time



hosts = "https://api.ourbit.com"
ourbit_key = "ob0vglFmsLo8XMExyw"
ourbit_secret = "672ec2ba47b649fbbd25efe609cd9c54"

granularity = 300
short_period = 5
long_period = 20
last_order_time = 0
last_order_type = None
test_balance = {"BTC": 0.0, "USDT": 405.7121}
last_condition = None
last_condition_count = 0
last_fetch_time = 0
is_new_timestamp = False

# Market Data
"""get kline"""
data = ourbit_spot_v3.ourbit_market(ourbit_hosts=hosts)


# Spot Trade
"""place an order"""
trade = ourbit_spot_v3.ourbit_trade(ourbit_key=ourbit_key, ourbit_secret=ourbit_secret, ourbit_hosts=hosts)

"""get spot account information"""
account = ourbit_spot_v3.ourbit_account(ourbit_key=ourbit_key, ourbit_secret=ourbit_secret, ourbit_hosts=hosts)

# def get_balance():

def get_current_price():
    kline = data.get_kline(params)
    return kline[-1][4]

def convert_list_to_df(kline):
    headers = ["Open time", "Open", "High", "Low", "Close", "Volume", "Close time", "Qute asset volume"]

    # Create DataFrame with specified headers
    df = pd.DataFrame(kline, columns=headers)

    df["Open time"] = df["Open time"].apply(lambda x: datetime.datetime.fromtimestamp(x/1000.0))
    # df["Close time"] = df["Close time"].apply(lambda x: datetime.datetime.fromtimestamp(x/1000.0))

    df["Close"] = df["Close"].apply(lambda x: float(x))

    return df

def get_balance():
    response = account.get_account_info()

    balance = {}
    for currency in response["balances"]:
        balance[currency["asset"]] = {}
        balance[currency["asset"]]["free"] = float(currency["free"])
        balance[currency["asset"]]["locked"] = float(currency["locked"])
    
    return balance

def trade_spot(side, price):
    price = float(price)

    # Calculate quantity
    if side == "buy":
        quantity = int(test_balance["USDT"] / price * 10000) / 10000
        test_balance["BTC"] = quantity
        test_balance["USDT"] = test_balance["USDT"] - quantity * price
    elif side == "sell":
        quantity = test_balance["BTC"]
        test_balance["BTC"] = 0.0
        test_balance["USDT"] = test_balance["USDT"] + quantity * price
    return test_balance



def calc_ma(df, window_size):
    close_df = df["Close"]

    df[f'MA_{window_size}']=close_df.rolling(window=window_size).mean()

    return df
    
def check_conditions(df):
    latest_row = df.iloc[-1]
    price = latest_row["Close"]
    
    is_above_MA5 = price > latest_row["MA_5"]
    is_above_MA20 = price > latest_row["MA_20"]

    if is_above_MA5 and is_above_MA20:
        global last_order_type
        if last_order_type == "sell":
            return "buy"
        elif last_order_type == None:
            last_order_type = "buy"
            return None
        else:
            return None
    
    else:
        if last_order_type == "buy":
            return "sell"
        elif last_order_type == None:
            last_order_type = "sell"
            return None
        else:
            return None



    
params = {
    'symbol': 'BTCUSDT',
    'interval': '1m',
    'limit': 50
}

# print(trade_spot("buy"))

#'''
# while True:
#     kline = data.get_kline(params)
#     df = convert_list_to_df(kline)

#     # Calcuate Moving Average
#     df = calc_ma(df, short_period)
#     df = calc_ma(df, long_period)

#     condition = check_conditions(df)
#     latest_row = df.iloc[-1]
#     # print(latest_row["Close"])
#     if condition and last_order_time != latest_row["Close time"]:
#         if condition == last_condition and last_condition_count >= 2:
#             last_order_time = latest_row["Close time"]
#             last_order_type = condition
#             last_condition_count = 0

#             balance = trade_spot(condition, latest_row["Close"])
            
#             print(f"{condition} at price {latest_row['Close']}")
#             print(balance)
#         elif condition == last_condition and last_condition_count < 2:
#             last_condition_count += 1
#         elif condition != last_condition:
#             last_condition = condition
#             last_condition_count = 0


#     time.sleep(0.5)
#'''
print(get_balance())

# print(account.get_account_info())