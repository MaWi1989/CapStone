from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
#from flask_marshmallow import Marshmallow
from flask_migrate import Migrate 
from flask_cors import CORS
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


app = Flask(__name__)


app.config.from_object(Config)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

CORS(app)

bootstrap = Bootstrap(app)


from friend_finder import routes, models

