import os

SECRET_KEY='shushbot'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Database
SQLALCHEMY_DATABASE_URI = os.getenv(
    'DATABASE_URL',
    'postgres://postgres:password@127.0.0.1:5432/postgres')
