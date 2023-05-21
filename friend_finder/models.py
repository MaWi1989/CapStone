from . import db, login
#from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
#import secrets
from flask_login import UserMixin, current_user
from flask_marshmallow import Marshmallow



ma = Marshmallow()

class User(db.Model, UserMixin):
    id = db.Column(db.String(40), primary_key = True)
    name = db.Column(db.String(100))
    key = db.Column(db.String(10))
    email = db.Column(db.String(150), nullable = False) 
    password = db.Column(db.String(200), nullable = False) 
    city = db.Column(db.String(100), nullable = True) 
    state = db.Column(db.String(100), nullable = True) 
    school = db.Column(db.String(300), nullable = True)
    grade = db.Column(db.String(20), nullable = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')

    def __init__(self, name, key, email, password, city, state, school, grade):
        self.id = self.set_id()
        self.name = name
        self.key = key
        self.email = email
        self.password = self.set_password(password)
        self.city = city
        self.state = state
        self.school = school
        self.grade = grade
        


    def set_id(self):
        return str(uuid.uuid4())
    
    # def check_key(self, key):
    #     signup_keys = [12345, 23456, 34567, 'abcde', 'bcdef']
    #     if key not in signup_keys:
    #         return "models.py: Not a valid signup key. Please contact your child's school to obtain a valid key."
    
    def set_password(self, password):
        return generate_password_hash(password)
    

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    
    def __repr__(self):
        return f"User {self.name} has been added to the database!"


@login.user_loader
def load_user(id):
    return User.query.get(id)



class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(80))
    message = db.Column(db.Text())
    date = db.Column(db.DateTime, default = datetime.utcnow)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable = False)

    def __init__(self, title, message, user_id):
        self.title = title
        self.message = message
        self.user_id = user_id

    def __repr__(self):
        return f"Post: {self.message}"


class PostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'message', 'date', 'user_id')


post_schema = PostSchema()
all_posts_schema = PostSchema(many=True)
