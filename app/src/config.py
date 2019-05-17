import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Config(object):
    DEBUG = True
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    FACEBOOK_APP_ID = os.getenv('FACEBOOK_APP_ID')
    FACEBOOK_APP_SECRET = os.getenv('FACEBOOK_APP_SECRET')
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO')

app_config = {
    'config': Config
}
