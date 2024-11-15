import os

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'postgresql://testuser:testPassword@localhost:5432/test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False