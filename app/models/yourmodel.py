from .. import db
class YourModel(db.Model):
    """
    Template model.
    """
    # non-database variables
    foo = "bar"
    
    # database fields
    id = db.Column('id', db.Integer, primary_key = True, autoincrement = True)
    
    # custom properties 
    # ensure that your private fields that should not be accessed directly begin with an _
    # like "_name"
    
    