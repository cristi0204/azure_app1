# this is the main app to load
import json, config, sqlite3, time
from flask import Flask, request, jsonify, render_template, g, current_app
#from app.XTBApi.api import Client as XTBApiClient
from xapiconnector import *

app = Flask(__name__)

# 

#//////    Binance client ///////////////////////
from binance.client import Client as BinanceClient
from binance.enums import *

BinanceClient = BinanceClient(config.BINANCE_API_KEY, config.BINANCE_API_SECRET)

def BinanceOrder(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print(f"sending order {order_type} - {side} {quantity} {symbol}")
        order = BinanceClient.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return order


# r = redis.Redis(host='localhost', port=6379, db=0)

###########  sqlite3   ########
conn = sqlite3.connect('trade.db')
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS signals (
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
        ticker,
        order_action,
        order_contracts,
        order_price,
        broker,
        transactionID,
        orderStatus
    )
""")
conn.commit()

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('trade.db')
        g.db.row_factory = sqlite3.Row

    return g.db


###########  Index Page   ########
@app.get('/')
def dashboard():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT * FROM signals
    """)
    signals = cursor.fetchall()

    return render_template('dashboard.html', signals=signals)

###########  Sample Webhook   ########
@app.post("/webhook")
def webhook():
    data = request.data

    if data:
#        r.publish('tradingview', data)

        data_dict = request.json

        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO signals (ticker, order_action, order_contracts, order_price) 
            VALUES (?, ?, ?, ?)
        """, (data_dict['ticker'], 
                data_dict['strategy']['order_action'], 
                data_dict['strategy']['order_contracts'],
                data_dict['strategy']['order_price']))

        db.commit()
#        return data
        return {
            "symbol": data_dict['ticker'],
            "action": data_dict['strategy']['order_action'],
            "contracts": data_dict['strategy']['order_contracts'],
            "price": data_dict['strategy']['order_price']
        }

    return {
        "code": "success"
    }

###########  Binance Webhook   ########
@app.route('/binance', methods=['POST'])
def BinanceWebhook():
    #print(request.data)
    data = json.loads(request.data)
    
    if data['passphrase'] != config.BINANCE_WEBHOOK_PASSPHRASE:
        return {
            "code": "error",
            "message": "Nice try, invalid passphrase"
        }

    side = data['strategy']['order_action'].upper()
    quantity = data['strategy']['order_contracts']
    symbol = data['ticker']
    order_response = BinanceOrder(side, quantity, symbol)

    if order_response:
        return {
            "code": "success",
            "message": "order executed"
        }
    else:
        print("order failed")

        return {
            "code": "error",
            "message": "order failed"
        }
    #print(request.data)
    # print(f"sending order {order_type} - {side} {quantity} {symbol}")

###########  XTB Webhook   ########
@app.route('/xtb', methods=['POST'])
def XTBWebhook():
    data = json.loads(request.data)   
    if data['passphrase'] != config.XTB_WEBHOOK_PASSPHRASE:
        return {
            "code": "error",
            "message": "Not Authorized"
        }

    side = data['strategy']['order_action'].upper()
    quantity = data['strategy']['order_contracts']
    symbol = data['ticker']
    XTBclient = APIClient()
    # connect to RR socket, login
    loginResponse = XTBclient.execute(loginCommand(userId=config.XTB_USER_ID, password=config.XTB_USER_PASS))
    logger.info(str(loginResponse)) 
    if(loginResponse['status'] == False):
        print('Login failed. Error code: {0}'.format(loginResponse['errorCode']))
        return
    # get ssId from login response
    ssid = loginResponse['streamSessionId']
    # second method of invoking commands
    #resp = XTBclient.commandExecute('getAllSymbols')
    #resp = XTBclient.commandExecute('getCurrentUserData')
    resp = XTBclient.commandExecute("getTrades", {"openedOnly":True})
    #resp = XTBclient.commandExecute("getSymbol", {"symbol":symbol})
    #sclient = APIStreamClient(ssId=ssid, tickFun=procTickExample, tradeFun=procTradeExample, profitFun=procProfitExample, tradeStatusFun=procTradeStatusExample)
    #sclient.subscribeTrades()
    #sclient.subscribePrices(['EURUSD', 'EURGBP', 'EURJPY'])
    #sclient.subscribeProfits()
    #time.sleep(5)
    # gracefully close streaming socket
    #sclient.disconnect()

    # print(request.data)
    # CHECK IF MARKET IS OPEN FOR EURUSD
    # order_response = XTBclient.check_if_market_open(symbol)
    #XTBclient.get_all_symbols()
    # BUY ONE VOLUME (FOR EURUSD THAT CORRESPONDS TO 100000 units)
    #order_response = XTBclient.open_trade(side, symbol, quantity)
    # SEE IF ACTUAL GAIN IS ABOVE 100 THEN CLOSE THE TRADE
    #trades = XTBclient.update_trades() # GET CURRENT TRADES
    # order_response = XTBclient.update_trades() # GET CURRENT TRADES
    #trade_ids = [trade_id for trade_id in trades.keys()]
    #for trade in trade_ids:
    #    actual_profit = XTBclient.get_trade_profit(trade) # CHECK PROFIT
    #    if actual_profit >= 100:
    #        client.close_trade(trade) # CLOSE TRADE
    ## CLOSE ALL OPEN TRADES
    #XTBclient.close_all_trades()
    # THEN LOGOUT
    XTBclient.disconnect()
    print(request.data)
 
    if resp:
        return {
            "code": "success",
            "message": "order executed"
        }
    else:
        print("order failed")

        return {
            "code": "error",
            "message": "order failed"
        }
    # THEN LOGOUT
    #XTBclient.logout()
    
    # print(f"sending order {order_type} - {side} {quantity} {symbol}")
