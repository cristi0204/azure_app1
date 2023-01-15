# this is the main app to load
import json, config, sqlite3, time
from flask import Flask, request, jsonify, render_template, g, current_app

app = Flask(__name__)

#///////  XTB     //////
#from XTBApi.api import Client as XTBApiClient

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
