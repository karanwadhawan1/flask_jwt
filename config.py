import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = ''
    SQLALCHEMY_DATABASE_URI = 'postgresql://db_user:karan123@localhost:5432/flask_auth'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY_ACCESS_TOKEN = 'secret_key_access_token'
    SECRET_KEY_REFRESH_TOKEN = 'secret_key_refresh_token'
