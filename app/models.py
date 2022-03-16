# This models.py file is responsible for everything database
# Primarily the instantiation of our ORM and the creation of our database models (aka tables/entities)

# import our orm
from flask_sqlalchemy import SQLAlchemy
# create the instance of our ORM (object relational mapper aka translator between python and SQL)
db = SQLAlchemy()

# tools for our models
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash
from uuid import uuid4

#import our LoginManager + tools
from flask_login import LoginManager, UserMixin
# create the instance of our login manager
login = LoginManager()

# necessary function for our login manager
@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# create our database model - essentially the python code for a SQL create table
class User(db.Model, UserMixin):
    # lay out our columns just like we would in a SQL create table query
    # column_name = db.Column(db.DataType(<options>), constraints)
    id = db.Column(db.String(50), primary_key=True)
    username = db.Column(db.String(15), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    password = db.Column(db.String(250), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __init__(self, username, email, password, first_name='', last_name=''):
        self.username = username
        self.email = email.lower()
        self.first_name = first_name
        self.last_name = last_name
        self.password = generate_password_hash(password)
        self.id = str(uuid4())


# new DB model for our animals
class Animal(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    sci_name = db.Column(db.String(100), unique=True, nullable=False)
    size = db.Column(db.String(50))
    weight = db.Column(db.Integer)
    diet = db.Column(db.String(250))
    habitat = db.Column(db.String(250))
    lifespan = db.Column(db.Integer)
    description = db.Column(db.String(255), nullable = False)
    image = db.Column(db.String(100))
    price = db.Column(db.Float(2), nullable=False)

    # when a user submits a POST request to create a new animal
    # they'll be sending us a python dictionary
    # we'll then use that to make our object
    def __init__(self, dict):
        """
        expected dict structure:
        {
            'name': <str>,
            'sci_name': <str>,
            'description': <str>,
            'price': <float>,
            'image': <str>,
            #### rest of k:v pairs optional
            'size': <str>,
            'weight': <int>,
            'diet': <str>,
            'habitat': <str>,
            'lifespan': <int>
        }
        """
        self.id = str(uuid4())
        self.name = dict['name'].title()
        self.sci_name = dict['sci_name'].title()
        self.description = dict['description']
        self.image = dict['image']
        self.price = dict['price']
        self.size = dict.get('size')
        self.weight = dict.get('weight')
        self.diet = dict.get('diet')
        self.habitat = dict.get('habitat')
        self.lifespan = dict.get('lifespan')

    # write a function to translate this object to a dictionary
    # role here is take self and return a dictionary containing K:V pairs for each attribute
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'sci_name': self.sci_name,
            'image': self.image,
            'price': self.price,
            'size': self.size,
            'weight': self.weight,
            'diet': self.diet,
            'habitat': self.habitat,
            'lifespan': self.lifespan
        }


