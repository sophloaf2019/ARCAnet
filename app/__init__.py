from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()

def form_to_dict(form):
    """Convert a Flask form object to a dictionary."""
    return {key: form.get(key) for key in form.keys()}

def create_app(config_class=Config):
    app = Flask(__name__)
    
    app.config.from_object(config_class)
    
    """
    Enable if you are requiring logins.
    The 'login_view' variable should point to the name of the function for user logins.
    
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'
    
    """

    db.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        from . import routes, models
        
        """
        Enable if you are requiring logins.
        
        Use @login_required on routes to make them need a login. It will direct them to login_manager.login_view, set above.
        
        @login_manager.user_loader
        def load_user(user_id):
            return models.user.User.query.get(int(user_id))
        """

        db.create_all()
        return app