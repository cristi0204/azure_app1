create new folder to contain the azure app an load it in vscode

create new python virtual env
 python3 -m venv .env

select python interpreter and python version (SHIFT+COMMAND+P)

create .gitignore file and add .env/ or * 

create "app" folder and jump in
create file __init__.py inside app folder -> this will be the main app to load
create "templates" folder and add the required files for flask templates (index.html + base.html)

```  test the app
export FLASK_APP="startup:app"
export FLASK_ENV=development
flask run
```
python3 -m pip freeze > requirements.txt

create startup.py in app root folder

go to run and debug -> create a launch.json file

we will need to do the same for azure app 
app configuration -> general settings -> startup command
gunicorn --bind=0.0.0.0 --timeout 600  startup:app --> save to restart the app


azure app functions deployment
https://www.youtube.com/playlist?list=PLx_MamJPwgQMhvVvrDzjjz-B87IGJQiPF


###tradingview webhook bot
Send TradingView alerts to Telegram, Discord, Slack, Twitter and Email.
https://github.com/fabston/TradingView-Webhook-Bot
Flask app receiving alerts from TradingView and automatically place an order or send the chart to Discord where you
https://github.com/lth-elm/TradingView-Webhook-Trading-Bot


https://github.com/IAMtheIAM/autoview-tradingview-chrome-docker-bot


## xtb
https://github.com/OlafSk/pyXTB
https://github.com/federico123579/XTBApi
http://developers.xstore.pro/api/wrappers/2.5.0


## binance

git repo
https://github.com/hackingthemarkets/tradingview-binance-strategy-alert-webhook
https://www.youtube.com/watch?v=gMRee2srpe8


Procfile  (file in git root)
web: gunicorn app:app

requirements.txt
flask
gunicorn
python-binance


tradingview strategy optimization bot
Let Python optimize the best stop loss and take profits for your TradingView strategy
https://github.com/TreborNamor/TradingView-Machine-Learning-GUI


tw alerts tool

https://github.com/alleyway/add-tradingview-alerts-tool

#####. XTB
https://github.com/OlafSk/pyXTB
https://github.com/federico123579/XTBApi
https://github.com/Saitama298/Python-XTB-API
https://github.com/tuxskar/PyXTBClient

//////////

/Alert message content for 3commas
ADAPERP_long_bot_start      = "{  \"action\": \"start_bot_and_start_deal\",  \"message_type\": \"bot\",  \"bot_id\": 7919106,  \"email_token\": \"d22045a7-624e-40c2-97c5-b8bb40c069c1\",  \"delay_seconds\": 0}"
ADAPERP_long_bot_stop       = "{  \"action\": \"close_at_market_price_all_and_stop_bot\",  \"message_type\": \"bot\",  \"bot_id\": 7919106,  \"email_token\": \"d22045a7-624e-40c2-97c5-b8bb40c069c1\",  \"delay_seconds\": 0}"
ADAPERP_short_bot_start     = "{  \"action\": \"start_bot_and_start_deal\",  \"message_type\": \"bot\",  \"bot_id\": 7919140,  \"email_token\": \"d22045a7-624e-40c2-97c5-b8bb40c069c1\",  \"delay_seconds\": 0}"
ADAPERP_short_bot_stop      = "{  \"action\": \"close_at_market_price_all_and_stop_bot\",  \"message_type\": \"bot\",  \"bot_id\": 7919140,  \"email_token\": \"d22045a7-624e-40c2-97c5-b8bb40c069c1\",  \"delay_seconds\": 0}"

if (LongBuy)
    strategy.entry(id="L", 
     direction=strategy.long,
     alert_message= ADAPERP_long_bot_start
     )
if (LongSell)
    strategy.close(id="L",
     alert_message= ADAPERP_long_bot_stop
     )

if (ShortBuy)
    strategy.entry(id="S",
     direction=strategy.short,
     alert_message=ADAPERP_short_bot_start
     )
if (ShortSell)
    strategy.close(id="S",
     alert_message=ADAPERP_short_bot_stop
     )


ADAPERP_long_bot_start      = "{  \"action\": \"start_bot_and_start_deal\",  \"message_type\": \"bot\",  \"bot_id\": 7919106,  \"email_token\": \"d22045a7-624e-40c2-97c5-b8bb40c069c1\",  \"delay_seconds\": 0}"
ADAPERP_long_bot_stop       = "{  \"action\": \"close_at_market_price_all_and_stop_bot\",  \"message_type\": \"bot\",  \"bot_id\": 7919106,  \"email_token\": \"d22045a7-624e-40c2-97c5-b8bb40c069c1\",  \"delay_seconds\": 0}"
ADAPERP_short_bot_start     = "{  \"action\": \"start_bot_and_start_deal\",  \"message_type\": \"bot\",  \"bot_id\": 7919140,  \"email_token\": \"d22045a7-624e-40c2-97c5-b8bb40c069c1\",  \"delay_seconds\": 0}"
ADAPERP_short_bot_stop      = "{  \"action\": \"close_at_market_price_all_and_stop_bot\",  \"message_type\": \"bot\",  \"bot_id\": 7919140,  \"email_token\": \"d22045a7-624e-40c2-97c5-b8bb40c069c1\",  \"delay_seconds\": 0}"

Long = "{\"passphrase\": \"somelongstring123\",\"ticker\": \"NATGAS\",\"strategy\": {\"order_action\": \"buy\",\"order_contracts\": 0.01,\"market_position\":\"long\",\"tp\": 0.0,\"sl\": 0.0}}"
Short = "{\"passphrase\": \"somelongstring123\",\"ticker\": \"NATGAS\",\"strategy\": {\"order_action\": \"sell\",\"order_contracts\": 0.01,\"market_position\":\"long\",\"tp\": 0.0,\"sl\": 0.0}}"
Close = "{\"passphrase\": \"somelongstring123\",\"ticker\": \"NATGAS\",\"strategy\": {\"order_action\": \"close\",\"order_contracts\": 0.01,\"market_position\":\"long\",\"tp\": 0.0,\"sl\": 0.0}}"

// -- Long Deal -->
if (longStartCondition)
    strategy.entry(id="L", direction = strategy.long, alert_message = longStartMessage )

if (longStopCondition)
    strategy.close("L", alert_message = longStopMessage)
// -- Short Deal -->
if (shortStartCondition)
    strategy.entry(id="S", direction = strategy.short, alert_message = shortStartMessage )
if (shortStopCondition)
    strategy.close(id="S", alert_message = shortStopMessage )
