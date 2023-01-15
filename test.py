# not working at this level, need to update init and api with app prefix
from app.XTBApi.api import Client as XTBClient
# FIRST INIT THE CLIENT
XTBclient = XTBClient()
# THEN LOGIN
#XTBclient.login("{user_id}", "{password}", mode={demo,real})
XTBclient.login("14255925", "P@rola123", mode="demo")
# CHECK IF MARKET IS OPEN FOR EURUSD
#XTBclient.check_if_market_open("ETHEREUM")
#XTBclient.get_all_symbols()
# BUY ONE VOLUME (FOR EURUSD THAT CORRESPONDS TO 100000 units)
#XTBclient.open_trade('sell', 'ETHEREUM', 1)
# SEE IF ACTUAL GAIN IS ABOVE 100 THEN CLOSE THE TRADE
trades = XTBclient.update_trades() # GET CURRENT TRADES
trade_ids = [trade_id for trade_id in trades.keys()]
for trade in trade_ids:
    actual_profit = XTBclient.get_trade_profit(trade) # CHECK PROFIT
#    if actual_profit >= 100:
#        client.close_trade(trade) # CLOSE TRADE
## CLOSE ALL OPEN TRADES
#XTBclient.close_all_trades()
# THEN LOGOUT
XTBclient.logout()

#    def trade_transaction(self, symbol, mode, trans_type, volume, stop_loss=0,
#
#                           take_profit=0, **kwargs):
"""
XTBclient = XTBClient()
XTBclient.login("14255925", "P@rola123", mode="demo")
XTBclient.check_if_market_open("ETHEREUM")
XTBclient.logout()
"""