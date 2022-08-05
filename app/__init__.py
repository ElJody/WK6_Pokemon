from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask import Flask
from config import Config
app = Flask(__name__)
app.config.from_object(Config)
#from app import routes
#from templates.models import User
db=SQLAlchemy(app)
migrate=Migrate(app,db)
from app import routes, models