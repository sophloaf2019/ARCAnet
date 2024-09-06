from .. import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    
    # database fields
    id = db.Column('id', db.Integer, primary_key = True, autoincrement = True)
    username = db.Column('username', db.String, unique = True)
    name = db.Column('name', db.String)
    password = db.Column('password', db.String)
    clearance = db.Column('clearance', db.String)

    assignment = db.Column('assignment', db.String)
    # Declassified
    # Sensitive
    # Confidential
    # Classified
    # Secret
    # Top Secret