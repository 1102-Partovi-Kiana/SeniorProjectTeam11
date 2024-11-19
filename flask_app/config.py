import os

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'postgresql://testuser:testPassword@localhost:5432/test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587 
    MAIL_USE_TLS = True 
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'officialwarerecovery@gmail.com'
    MAIL_PASSWORD = 'wqyo psqt qams pmhk'
