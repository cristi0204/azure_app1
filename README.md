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





tradingview strategy optimization bot
Let Python optimize the best stop loss and take profits for your TradingView strategy
https://github.com/TreborNamor/TradingView-Machine-Learning-GUI


tw alerts tool

https://github.com/alleyway/add-tradingview-alerts-tool