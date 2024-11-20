from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False) 
    password = db.Column(db.LargeBinary, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role_id = db.Column(db.Integer, nullable=False)