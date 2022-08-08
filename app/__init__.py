from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask import Flask
from flask_login import LoginManager
#from flask_httpauth import HTTPBasicAuth
from config import Config
app = Flask(__name__)
app.config.from_object(Config)
#from app import routes
#from templates.models import User
db=SQLAlchemy(app)
migrate=Migrate(app,db)
login = LoginManager(app,db)


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate.init_app(app, db)
login.init_app(app)
login.login_view = 'auth.login'
login.login_message = 'Please enter your email and password below'
login.login_message_category = 'warning'
    
from app import routes, models