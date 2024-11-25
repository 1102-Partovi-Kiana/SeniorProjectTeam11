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

class Classes(db.Model):
    __tablename__ = 'classes'
    class_id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(100), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)

    course = db.relationship('Courses', backref='classes', lazy=True)
    user = db.relationship('User', backref='classes', lazy=True)