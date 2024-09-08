from .. import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    
    # database fields
    id = db.Column('id', db.Integer, primary_key = True, autoincrement = True)
    username = db.Column('username', db.String, unique = True)
    name = db.Column('name', db.String)
    password = db.Column('password', db.String)
    clearance = db.Column('clearance', db.Integer)

    assignment = db.Column('assignment', db.String)
    # Declassified   0
    # Sensitive      1
    # Confidential   2
    # Classified     3
    # Secret         4
    # Top Secret     5