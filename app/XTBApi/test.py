from api import Client
# FIRST INIT THE CLIENT
client = Client()
# THEN LOGIN
#client.login("{user_id}", "{password}", mode={demo,real})
client.login("14255925", "P@rola123", mode="demo")
# CHECK IF MARKET IS OPEN FOR EURUSD
#client.check_if_market_open("ETHEREUM")
#client.get_all_symbols()
# BUY ONE VOLUME (FOR EURUSD THAT CORRESPONDS TO 100000 units)
#client.open_trade('sell', 'ETHEREUM', 1)
# SEE IF ACTUAL GAIN IS ABOVE 100 THEN CLOSE THE TRADE
trades = client.update_trades() # GET CURRENT TRADES
#trade_ids = [trade_id for trade_id in trades.keys()]
#for trade in trade_ids:
#    actual_profit = client.get_trade_profit(trade) # CHECK PROFIT
#    if actual_profit >= 100:
#        client.close_trade(trade) # CLOSE TRADE
## CLOSE ALL OPEN TRADES
#client.close_all_trades()
# THEN LOGOUT
client.logout()

#    def trade_transaction(self, symbol, mode, trans_type, volume, stop_loss=0,
#                          take_profit=0, **kwargs):