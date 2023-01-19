# this is the main app to load
import json, config, sqlite3, time
from flask import Flask, request, jsonify, render_template, g, current_app
#from app.XTBApi.api import Client as XTBApiClient
#from xapiconnector import *
from pyXTB import trader

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
###########  XTB Status   ########
@app.route('/xtbstatus', methods=['POST'])
def xtbstatus():
    pyxtb = trader()
    pyxtb.login(id=config.XTB_USER_ID,password=config.XTB_USER_PASS)
    return pyxtb._opened_trades
    #result = json.loads(pyxtb.get_opened_trades())
    #return result['returnData']['message']
    #print (pyxtb)
    #return pyxtb._balance #'1' #render_template('dashboard.html', signals=signals)

###########  XTB Status   ########
@app.route('/xtborders', methods=['POST'])
def xtborder():
    data = json.loads(request.data)
    pyxtb = trader()
    pyxtb.login(id=config.XTB_USER_ID,password=config.XTB_USER_PASS)    

    if data['passphrase'] != config.XTB_WEBHOOK_PASSPHRASE:
        return {
            "code": "error",
            "message": "Invalid peer"
        }

    symbol = data['ticker']
    side = data['strategy']['order_action'].upper()
    order_action = data['strategy']['order_action'].upper()
    position = data['strategy']['market_position']
    quantity = data['strategy']['order_contracts']
    #quantity = "0.01"
    tp = data['strategy']['tp']
    sl = data['strategy']['sl']
    #print('Order data - Symbol:  ' + str(symbol) + '  Action ' + str(order_action) + '  Quantity ' + str(quantity))
    #print (order_action)
    if order_action == "BUY":
        xtborder = pyxtb.buy_symbol(symbol,quantity) #,tp,sl) 
        #result = json.loads(xtborder)
        #print (xtborder)
        return xtborder
        
    elif order_action == "SELL":
        xtborder = pyxtb.sell_symbol(symbol,quantity) #,tp,sl)
        #result = json.loads(xtborder)
        return xtborder
    elif order_action: 
        xtborder = pyxtb.close_all_symbol(symbol)
        #result = json.loads(xtborder)
        #print (closeorder)
        #return #result['returndata']['order']
        if not xtborder:
            return ' XTB Order No trades to close'
        return xtborder
    return 'OK'
    #print(request.data)
    # print(f"sending order {order_type} - {side} {quantity} {symbol}")

###########  XTB Status   ########
@app.route('/xtbgetsymbol', methods=['POST'])
def xtbgetsymbol():
    data = json.loads(request.data)
    pyxtb = trader()
    pyxtb.login(id=config.XTB_USER_ID,password=config.XTB_USER_PASS)    

    if data['passphrase'] != config.XTB_WEBHOOK_PASSPHRASE:
        return {
            "code": "error",
            "message": "Invalid peer"
        }

    symbol = data['ticker']
    symboldata = pyxtb.get_symbol_data(symbol)
    return symboldata