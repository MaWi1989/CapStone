import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(basedir, '.env'))

class Config(object):

    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_APP = os.environ.get('FLASK_ENV')
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you'll never guess"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MIDIFICATIONS = False 
    POSTS_PER_PAGE = 5