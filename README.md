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

