
from websocket import create_connection
import json
import config
# https://github.com/OlafSk/pyXTB

id=config.XTB_USER_ID
password=config.XTB_USER_PASS

class trader:

    def __init__(self, webaddres = "wss://ws.xtb.com/demo"):
        self.ws = create_connection("wss://ws.xtb.com/demo")
        self._balance = {}
        self._opened_trades = {}
    def login(self, id, password):
        d = {
        	"command" : "login",
        	"arguments" : {
        		"userId" : id,
        		"password": password
        	},
        	"customTag": "my_login_command_id"}
        self.ws.send(json.dumps(d))
        result = json.loads(self.ws.recv())
        if result['status']:
            print("Login - success")
            self.get_opened_trades()
            self.refresh_balance()
            return result
        elif not result['status']:
            print("Login - failed")
            return result

    def refresh_balance(self):
        print ('Checking Balance')
        d = {"command": "getMarginLevel"}
        self.ws.send(json.dumps(d))
        self._balance = json.loads(self.ws.recv())['returnData']
        #return

    def sell_symbol(self, symbol, volume, tp = 0.0, sl = 0.0):
        price = self.get_symbol_data(symbol)['returnData']['bid']
        print ({"sell_symbol - Short entering price": price})
        TRADE_TRANS_INFO = {
            "cmd": 1,
            "customComment": "my_comment",
            "expiration": 0,
            "offset": 0,
            "order": 0,
            "price": price,
            "sl" : sl,
            "symbol": symbol,
            "tp" : tp,
            "type": 0,
            "volume": volume}

        query = {
           "command": "tradeTransaction",
           "arguments": {
                      "tradeTransInfo": TRADE_TRANS_INFO}}
        self.ws.send(json.dumps(query))
        result = json.loads(self.ws.recv())
        order_number = result['returnData']['order']
        if result['status']:
            print("sell_symbol - Sell Order sent")
            return result
        else:
            print("sell_symbol - Sell Order Error")
            #return {"order": "error"}
        message = self._check_trade_status(order_number)
        print(message)
        print('sell_symbol exit')
        return {"trade id": message}


    def buy_symbol(self, symbol, volume, tp = 0.0, sl = 0.0):
        price = self.get_symbol_data(symbol)['returnData']['ask']
        print ({"buy_symbol - Long entering price": price})
        TRADE_TRANS_INFO = {
            "cmd": 0,
            "customComment": "my_comment",
            "expiration": 0,
            "offset": 0,
            "order": 0,
            "price": price,
            "sl" : sl,
            "symbol": symbol,
            "tp" : tp,
            "type": 0,
            "volume": volume}

        query = {
	       "command": "tradeTransaction",
	       "arguments": {
		              "tradeTransInfo": TRADE_TRANS_INFO}}
        self.ws.send(json.dumps(query))
        result = json.loads(self.ws.recv())
        order_number = result['returnData']['order']
        if result['status']:
            print("buy_symbol - Buy Order Sent")
            return result
        else:
            print("buy_symbol - Buy Order Error")
        message = self._check_trade_status(order_number)
        print(message)
        print('buy_symbol - exit')

    def get_symbol_data(self, symbol):
        print ('get_symbol_data - Getting symbol data')
        query  = {
        	"command": "getSymbol",
        	"arguments": {
        		"symbol": symbol}}
        self.ws.send(json.dumps(query))
        return json.loads(self.ws.recv())

    def get_opened_trades(self, opened_only = True):
        print ('get_opened_trades - Getting open trades get_opened_trades')
        query = {
                "command": "getTrades",
                "arguments": {
                	"openedOnly": opened_only}}
        self.ws.send(json.dumps(query))
        result = json.loads(self.ws.recv())['returnData']
        print (result)
        for trade in range(len(result)):
            info = result[trade]
            single_trade_details = {
                    'symbol': info["symbol"],
                    'open_price': info['open_price'],
                    'volume': info['volume'],
                    'profit': info['profit'],
                    'order_open': info['order'],
                    'order_close': info['order']
            }
            if info['cmd'] == 0:
                single_trade_details['position'] = "long"
            else:
                single_trade_details['position'] = "short"
            try:
                self._opened_trades[info['symbol']].append(single_trade_details)
            except:
                self._opened_trades[info['symbol']] = [single_trade_details]
        print ('exiting get_opened_trades')


    def _check_trade_status(self, order):
        print ('_check_trade_status - Checking trade status')
        query = {
                "command": "tradeTransactionStatus",
                "arguments": {
                        "order": order}}
        self.ws.send(json.dumps(query))
        result = json.loads(self.ws.recv())
        return result['returnData']['message']

    def print_opened_trades(self):
        print ('print_opened_trades - Printing open trades')
        pass

    def close_all_symbol(self, symbol):
        price = self.get_symbol_data(symbol)['returnData']['ask']
        print('\n\close_all_symbol - Closing trades for simbol\n')
        closeALL = self._opened_trades[symbol]
        print ({'type': type(closeALL)})
        print ({'lenght of list': len(closeALL)})
        # if(self._opened_trades[symbol] is None):
        #     print ('close_all_symbol - closeALL is None')
        #     return
        if closeALL:
            print ('\n\n close_all_symbol - There are active trades\n')
            #return 'There are active trades'
            for i in range(len(self._opened_trades[symbol])):
                volume = self._opened_trades[symbol][i]['volume']
                order = self._opened_trades[symbol][i]['order_close']
                print ('\n\n close_all_symbol - Printing the transaction ids')
                print (order)
                TRADE_TRANS_INFO = {
                    "cmd": 0,
                    "customComment": "my_comment",
                    "expiration": 0,
                    "offset": 0,
                    "order": order,
                    "price": price,
                    "sl" : 0,
                    "symbol": symbol,
                    "tp" : 0,
                    "type": 2,
                    "volume": volume}
                query = {
    	           "command": "tradeTransaction",
        	       "arguments": {
        		              "tradeTransInfo": TRADE_TRANS_INFO}}
                print ('\n\n close_all_symbol - Printing the message sent to XTB')
                print (query)
                self.ws.send(json.dumps(query))
                result = json.loads(self.ws.recv())
                print ('\n\n close_all_symbol - Printing the result')
                print(result)
                return result
            del self._opened_trades[symbol]
        else :
            print ('\n\n close_all_symbol - There are no open trades\n')
            return 'close_all_symbol - There are no open trades'
        
    #This has to delete entry in self._opened_trades as well
    def close_trade(self, order, symbol):
        price = self.get_symbol_data(symbol)['returnData']['ask']
        for i in range(len(self._opened_trades[symbol])):
            if self._opened_trades[symbol][i]['order_close'] == order:
                volume = self._opened_trades[symbol][i]['volume']
                number = i
        TRADE_TRANS_INFO = {
            "cmd": 0,
            "customComment": "my_comment",
            "expiration": 0,
            "offset": 0,
            "order": order,
            "price": price,
            "sl" : 0,
            "symbol": symbol,
            "tp" : 0,
            "type": 2,
            "volume": volume}

        query = {
	       "command": "tradeTransaction",
	       "arguments": {
		              "tradeTransInfo": TRADE_TRANS_INFO}}
        self.ws.send(json.dumps(query))
        result = json.loads(self.ws.recv())
        #print(result)
        order_number = result['returnData']['order']
        if result['status']:
            print("close_trade - Order sent")
            del self._opened_trades[symbol][number]
            return result
        else:
            print("close_trade - Error with sending order")
        message = self._check_trade_status(order_number)
        print(message)
        return message