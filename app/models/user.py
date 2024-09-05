from .. import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    
    # database fields
    id = db.Column('id', db.Integer, primary_key = True, autoincrement = True)
    username = db.Column('username', db.String, unique = True)
    name = db.Column('name', db.String)
    password = db.Column('password', db.String)
    clearance = db.Column('clearance', db.String)

    @property
    def clearance_symbol(self):
        if self.clearance == 'Declassified':
            return "●"
        elif self.clearance == 'Sensitive':
            return "⚊"
        elif self.clearance == 'Confidential':
            return "⚌"
        elif self.clearance == 'Classified':
            return "⚎"
        elif self.clearance == 'Secret':
            return "⚏"
        elif self.clearance == 'Top Secret':
            return '█'

    assignment = db.Column('assignment', db.String)
    # Declassified
    # Sensitive
    # Confidential
    # Classified
    # Secret
    # Top Secret