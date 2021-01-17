live_trade = True
pair            = "LINK" + "USDT"
quantity        = 1
leverage        = 75
threshold       = 0.15
stoplimit       = 0.15
callbackRate    = 0.3
round_decimal   = 4

import os
import time
import socket
import requests
import urllib3
from datetime import datetime
from binance.client import Client
from binance.exceptions import BinanceAPIException
def get_timestamp(): return int(time.time() * 1000)

def get_current_trend(): # >>> UP_TREND // DOWN_TREND // NO_TRADE_ZONE
    if get_2hour() == "DOWN_TREND" and get_6hour() == "DOWN_TREND":
        trend = "DOWN_TREND"
        print("Current TREND    :   🩸 DOWN_TREND 🩸")
    elif get_2hour() == "UP_TREND" and get_6hour() == "UP_TREND":
        trend = "UP_TREND"
        print("Current TREND    :   🥦 UP_TREND 🥦")
    else:
        trend = "NO_TRADE_ZONE"
        print("Current TREND    :   😴 NO_TRADE_ZONE 😴")
    return trend

def get_current_minute(): # >>> RED_CANDLE // GREEN_CANDLE // WEAK_RED // WEAK_GREEN // RED_INDECISIVE // GREEN_INDECISIVE // SOMETHING_IS_WRONG
    klines = client.futures_klines(symbol=pair, interval=Client.KLINE_INTERVAL_1MINUTE, limit=3)

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), round_decimal)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), round_decimal)
    previous_Open   = round(((first_run_Open + first_run_Close) / 2), round_decimal)
    previous_Close  = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), round_decimal)
    
    current_Open    = round(((previous_Open + previous_Close) / 2), round_decimal)
    current_Close   = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[2][3]) + float(klines[2][4])) / 4), round_decimal)
    current_High    = max(float(klines[2][2]), current_Open, current_Close)
    current_Low     = min(float(klines[2][3]), current_Open, current_Close)

    price_movement = (current_High - current_Low) / current_Open * 100

    if (current_Open == current_High):          
        if (price_movement >= threshold):
            minute_candle = "RED_CANDLE"
            print("Current MINUTE   :   🩸🩸🩸 RED 🩸🩸🩸")
        else:
            minute_candle = "WEAK_RED"
            print("Current MINUTE   :   🩸 WEAK_RED 🩸")
    elif (current_Open == current_Low):         
        if (price_movement >= threshold):
            minute_candle = "GREEN_CANDLE"
            print("Current MINUTE   :   🥦🥦🥦 GREEN 🥦🥦🥦")
        else:
            minute_candle = "WEAK_GREEN"
            print("Current MINUTE   :   🥦 WEAK_GREEN 🥦")
    else:
        if (current_Open > current_Close):
            print("Current MINUTE   :   🩸 RED_INDECISIVE 🩸")
            minute_candle = "RED_INDECISIVE"
        elif (current_Close > current_Open):
            print("Current MINUTE   :   🥦 GREEN_INDECISIVE 🥦")
            minute_candle = "GREEN_INDECISIVE"
        else:
            minute_candle = "SOMETHING_IS_WRONG"
            print("❗SOMETHING_IS_WRONG in get_minute_candle()❗")
    return minute_candle

def get_2hour(): # >>> UP_TREND // DOWN_TREND // NO_TRADE_ZONE
    klines = client.futures_klines(symbol=pair, interval=Client.KLINE_INTERVAL_2HOUR, limit=3)

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), round_decimal)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), round_decimal)
    previous_Open   = round(((first_run_Open + first_run_Close) / 2), round_decimal)
    previous_Close  = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), round_decimal)

    current_Open    = round(((previous_Open + previous_Close) / 2), round_decimal)
    current_Close   = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[2][3]) + float(klines[2][4])) / 4), round_decimal)
    current_High    = max(float(klines[2][2]), current_Open, current_Close)
    current_Low     = min(float(klines[2][3]), current_Open, current_Close)

    if (current_Open == current_High):
        trend = "DOWN_TREND"
        # print("Current TREND    :   🩸 DOWN_TREND 🩸")
    elif (current_Open == current_Low):
        trend = "UP_TREND"
        # print("Current TREND    :   🥦 UP_TREND 🥦")
    else:
        trend = "NO_TRADE_ZONE"
        # print("Current TREND    :   😴 NO_TRADE_ZONE 😴")
    return trend

def get_6hour(): # >>> UP_TREND // DOWN_TREND // NO_TRADE_ZONE
    klines = client.futures_klines(symbol=pair, interval=Client.KLINE_INTERVAL_6HOUR, limit=3)

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), round_decimal)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), round_decimal)
    previous_Open   = round(((first_run_Open + first_run_Close) / 2), round_decimal)
    previous_Close  = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), round_decimal)

    current_Open    = round(((previous_Open + previous_Close) / 2), round_decimal)
    current_Close   = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[2][3]) + float(klines[2][4])) / 4), round_decimal)
    current_High    = max(float(klines[2][2]), current_Open, current_Close)
    current_Low     = min(float(klines[2][3]), current_Open, current_Close)

    if (current_Open == current_High):
        trend = "DOWN_TREND"
        # print("Current TREND    :   🩸 DOWN_TREND 🩸")
    elif (current_Open == current_Low):
        trend = "UP_TREND"
        # print("Current TREND    :   🥦 UP_TREND 🥦")
    else:
        trend = "NO_TRADE_ZONE"
        # print("Current TREND    :   😴 NO_TRADE_ZONE 😴")
    return trend

def get_position_info(): # >>> LONGING // SHORTING // NO_POSITION
    positionAmt = float(client.futures_position_information(symbol=pair, timestamp=get_timestamp())[0].get('positionAmt'))
    if (positionAmt > 0):
        position = "LONGING"
    elif (positionAmt < 0):
        position = "SHORTING"
    else:
        position = "NO_POSITION"
    print("Current Position :   " + position)
    return position 

def trade_action(position_info, trend, minute_candle):
    if position_info == "LONGING":
        if (minute_candle == "RED_CANDLE"):
            if live_trade: client.futures_create_order(symbol=pair, side="SELL", type="MARKET", quantity=quantity, timestamp=get_timestamp())
            print("Action           :   💰 CLOSE_LONG 💰")
        else:
            print("Action           :   ✊🥦 HOLDING_LONG 🥦💪")

    elif position_info == "SHORTING":
        if (minute_candle == "GREEN_CANDLE"):
            if live_trade: client.futures_create_order(symbol=pair, side="BUY", type="MARKET", quantity=quantity, timestamp=get_timestamp())
            print("Action           :   💰 CLOSE_SHORT 💰")
        else:
            print("Action           :   ✊🩸 HOLDING_SHORT 🩸💪")

    else:
        client.futures_cancel_all_open_orders(symbol=pair, timestamp=get_timestamp())
        if trend == "UP_TREND":
            if (minute_candle == "GREEN_CANDLE"):
                if live_trade: 
                    client.futures_create_order(symbol=pair, side="BUY", type="MARKET", quantity=quantity, timestamp=get_timestamp())
                    print("Action           :   🚀 GO_LONG 🚀")
                    markPrice = float(client.futures_position_information(symbol=pair, timestamp=get_timestamp())[0].get('markPrice'))
                    stopPrice = round((markPrice - (markPrice * stoplimit / 100)), (round_decimal - 1))
                    client.futures_create_order(symbol=pair, side="SELL", type="STOP_MARKET", stopPrice=stopPrice, quantity=quantity, timeInForce="GTC", timestamp=get_timestamp())
                    # client.futures_create_order(symbol=pair, side="SELL", type="LIMIT", price=stopPrice, quantity=quantity, timeInForce="GTC", timestamp=get_timestamp())
                    client.futures_create_order(symbol=pair, side="SELL", type="TRAILING_STOP_MARKET", callbackRate=callbackRate, reduceOnly=True, quantity=quantity, timestamp=get_timestamp())
            else:
                print("Action           :   🐺 WAIT 🐺")

        elif trend == "DOWN_TREND":
            if (minute_candle == "RED_CANDLE"):
                if live_trade: 
                    client.futures_create_order(symbol=pair, side="SELL", type="MARKET", quantity=quantity, timestamp=get_timestamp())
                    print("Action           :   💥 GO_SHORT 💥")
                    markPrice = float(client.futures_position_information(symbol=pair, timestamp=get_timestamp())[0].get('markPrice'))
                    stopPrice = round((markPrice + (markPrice * stoplimit / 100)), (round_decimal - 1))
                    client.futures_create_order(symbol=pair, side="BUY", type="STOP_MARKET", stopPrice=stopPrice, quantity=quantity, timeInForce="GTC", timestamp=get_timestamp())
                    # client.futures_create_order(symbol=pair, side="BUY", type="LIMIT", price=stopPrice, quantity=quantity, timeInForce="GTC", timestamp=get_timestamp())
                    client.futures_create_order(symbol=pair, side="BUY", type="TRAILING_STOP_MARKET", callbackRate=callbackRate, reduceOnly=False, quantity=quantity, timestamp=get_timestamp())
            else:
                print("Action           :   🐺 WAIT 🐺")
        else:
            print("Action           :   🐺 WAIT 🐺")

# Get environment variables && Initial Setup
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)
client.futures_change_leverage(symbol=pair, leverage=leverage, timestamp=get_timestamp())

while True:
    try:
        trade_action(get_position_info(), get_current_trend(), get_current_minute())
    except (BinanceAPIException, 
            ConnectionResetError, 
            socket.timeout,
            urllib3.exceptions.ProtocolError, 
            urllib3.exceptions.ReadTimeoutError,
            requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout) as e:

        if not os.path.exists("Error_Message"): os.makedirs("Error_Message")
        with open((os.path.join("Error_Message", pair , ".txt")), "a") as error_message:
            error_message.write("[!] " + pair + " - " + "Created at : " + datetime.today().strftime("%d-%m-%Y @ %H:%M:%S") + "\n")
            error_message.write(str(e) + "\n\n")
        continue

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")
    time.sleep(5)