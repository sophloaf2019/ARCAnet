import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RECENT_LOGS_COUNT = int(os.environ.get('RECENT_LOGS_COUNT', 5))
    SERVER_NAME= "localhost:5000"