from binance.client import Client
from binance.enums import *
# import matplotlib.pyplot as plt
import talib
import numpy as np
import requests
# import math
# x = float('nan')
# math.isnan(x)


try:
    from config import *
except:
    from config_prog import *



# try:
    # import config_dev
# except:
#   import config_prod environment variable @ cloud
#   import os ---> os.getenv('apikey')


client = Client(mine_key, mine_secret)

# symbols = "BTCUSDT"

# ORDER @ MARKET

def SendLineMessage(message):
    # urlLine_noitfy = 'https://notify-api.line.me/api/notify'
    # token='shLHko2YeIhcRBoOqNa6v3zl0Q6JBq2tOTzwZU2yVng'
    # header = {
    #         'content-type':
    #         'application/x-www-form-urlencoded',
    #         'Authorization':'MineBit+Anonymous'+token
    #        }
    # return requests.post(urlLine_noitfy,headers=header,data=message)
        playload ={'message':message}
        return _LineNofify(playload)

# msg={'message':'BUY COMPLETE'}
# SendLineMessage(msg)


# def SendLineSticker(sticker):
#     urlLine_noitfy = 'https://notify-api.line.me/api/notify'
#     token='shLHko2YeIhcRBoOqNa6v3zl0Q6JBq2tOTzwZU2yVng'
#     header = {
#             'content-type':
#             'application/x-www-form-urlencoded',
#             'Authorization':'MineBit+Anonymous'+token
#            }   
#     return requests.post(urlLine_noitfy,headers=header,data=sticker)

def SendLineSticker(stickerPackageID,stickerID):
    playlod = {'message':"",'stickerPackageId':stickerPackageID,'stickerId':stickerID}
    return _LineNofify(playlod)

def _LineNofify(playload,file=None):
    import requests
    urlLine_noitfy='https://notify-api.line.me/api/notify'
    token='shLHko2YeIhcRBoOqNa6v3zl0Q6JBq2tOTzwZU2yVng'
    header = {
            'content-type':
            'application/x-www-form-urlencoded',
            'Authorization':'MineBit+Anonymous'+token
           }
    return requests.post(urlLine_noitfy,headers=header,data=playload,files=file) 


def PlaceBUY(amount,symbol):
    candles = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_5MINUTE , limit =1)
    print(candles[0][4]) # OHLCV...
    close = candles[0][4]
    # if float(close)*amount < 10: #0.04
    if float(close)*amount < 0.05:
        return print("NOT ENOUGHT MINIMUM PLACE ORDER")
    # client.order_market_buy(
    # symbol=symbol,
    # quantity=str(amount))
    # client.order_limit_buy(symbol=symbol,quantity=str(amount)) #buy limit
    client.create_test_order(symbol=symbol,quantity=str(amount))
    # > 10USDT
    print("BUY COMPLETE")
    msg={'message':'BUY COMPLETE'+symbol+amount}
    #https://developers.line.biz/en/docs/messaging-api/sticker-list/#sticker-definitions
    # sticker={'message':"",'stickerPackageId':11537,'stickerId':52002735} #rabbit nice
    # SendLineSticker(sticker)
    # SendLineMessage(msg)

    _LineNofify(msg)
    SendLineSticker(11537,52002735)

# ORDER @ MARKET
def PlaceSELL(symbol):
    n=3
    trades = client.get_my_trades(symbol=symbol)
    
    while True:
        try:
            qty = float(trades[0]["qty"]) - float(trades[0]["commission"])
            qty = str(qty)[:n]
            # client.order_market_sell(
            # symbol=symbol,
            # quantity=str(qty))

            client.order_limit_sell(symbol=symbol,quantity=str(qty)) #sell limit market
            
            # > 10USDT
            print("SELL COMPLETE")
            # Line Nonify
            msg={'message':'SELL COMPLETE'+symbol}
            #https://developers.line.biz/en/docs/messaging-api/sticker-list/#sticker-definitions
            # sticker={'message':"",'stickerPackageId':11537,'stickerId':52002740}#rabbit ok
            # SendLineSticker(sticker)
            # SendLineMessage(msg)
            _LineNofify(msg)
            SendLineSticker(11537,52002740)
            return  

        except:
            n = n-1
            pass


def SIGNALS_BY_SYMBOLS(symbols):
    klines = client.get_historical_klines(symbols,Client.KLINE_INTERVAL_5MINUTE,"100 minutes ago UTC")    
    # closes = [float(i[4]) for i in klines]
    closes = [float(i[8]) for i in klines]
    closes = np.array(closes)
    #list comprehension
    # for i in klines ....
    # append each to list
    # print(closes)

    ema12 = talib.EMA(closes,timeperiod=12)
    ema26 = talib.EMA(closes,timeperiod=26)

    rsi = talib.RSI(closes, timeperiod=14)

    # figure => graph
    # fig = plt.figure()
    # axes = fig.add_axes([0.1,0.1,0.8,0.8])
    # axes.set_xlabel("1min time frame")
    # axes.set_ylabel("PRICE {}".format(symbols))

    # plt.plot(closes,"--",color="grey",label="Price")
    # plt.plot(ema12,"-",color="green",label="ema12")
    # plt.plot(ema26,"-",color="red",label="ema26")
    # #plt.plot(rsi,"-",color="yellow",label="rsi")


    
    # #cross over / cross under

    # crossover = [] #buy
    # crossunder = [] #sell


    # for index,val in enumerate(zip(ema12,ema26)):
    #     i = val[0] #[(1,2),(2,3)]
    #     j = val[1]
    #     #print(i," : ",j)
    #     #crossover
    #     if (ema12[index-1] < ema26[index-1]) and (i > j):
    #         print("BULLISH HERE {}".format(symbols))
    #         #คำนวณจำนวนเงินก่อน!!
    #         #PlaceBUY()
    #         # buy order here
    #         crossover.append(i) #จุดที่มีการครอส cross
    #     elif (ema12[index-1] > ema26[index-1]) and (i < j):
    #         print("BEARISH HERE {}".format(symbols))
    #         # sell order here
    #         #PlaceSELL()
    #         crossunder.append(i) #จุดที่มีการครอส cross

    #     else:
    #         crossover.append(None)
    #         crossunder.append(None)
    #         #print("NO SIGNALS FOR {}".format(symbols))
        
        
    # crossover = np.array(crossover)
    # crossunder = np.array(crossunder)


    # plt.plot(crossover,"x",color="green",label="BULLISH")
    # plt.plot(crossunder,"x",color="red",label="BEARISH")

    # plt.legend(loc="upper left")
    # plt.show()
    
    
    
    #Signals alertBUY
    BUY = (ema12[-2] < ema26[-2]) and (ema12[-1] > ema26[-1]) #bullish cross
    SELL = (ema12[-2] > ema26[-2]) and (ema12[-1] < ema26[-1]) #bearish cross
    
    Oversold = rsi[-1] < 30
    Overbought = rsi[-1] > 70
    
    if Oversold: print("{} OVERSOLD RSI < 30".format(symbols))
    elif Overbought: print("{} OVERBOUGHT RSI > 70".format(symbols))
    else: print("{} MIDDLE 30 < RSI < 70".format(symbols))
    
    
    price = closes[-1]
    # usd = 15
    bnb = 0.04 #minimumn order size
    # My BNB = 0.16  I can buy = 0.0358 bnb
    # amount = float(usd/price)
    amount = float(bnb/price)

    
    
    if BUY: return PlaceBUY(amount=amount,symbol=symbols)
    elif SELL: return PlaceSELL(symbol=symbols)
    else: return "NONE"