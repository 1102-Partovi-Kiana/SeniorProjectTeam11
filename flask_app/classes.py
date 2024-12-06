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

    classes = db.relationship('Classes', backref='user', lazy=True)

class Classes(db.Model):
    __tablename__ = 'classes'
    class_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    class_course_code = db.Column(db.String(100), nullable=False)
    class_section_number = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True) 

class ClassCodes(db.Model):
    __tablename__ = 'class_codes'
    class_code_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'), nullable=False)
    class_code = db.Column(db.String(15), nullable=False, unique=True)
    
    class_ = db.relationship('Classes', backref=db.backref('class_codes', lazy=True))

class Enrollment(db.Model):
    __tablename__ = 'enrollment'

    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'), nullable=False)

    class_ = db.relationship('Classes', backref=db.backref('enrollments', lazy=True))
    user = db.relationship('User', backref=db.backref('enrollments', lazy=True))

class StudentAssignedCourses(db.Model):
    __tablename__ = 'student_assigned_courses'

    student_assigned_courses_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    user = db.relationship('User', backref=db.backref('assigned_courses', lazy=True))
    course = db.relationship('Courses', backref=db.backref('assigned_students', lazy=True))


class Courses(db.Model):
    __tablename__ = 'courses'

    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100))
    course_desc = db.Column(db.String(1000))
    section_number = db.Column(db.String(10))
    level = db.Column(db.String(50))
    certificate = db.Column(db.Boolean, default=False)
    length = db.Column(db.String(20))
    route = db.Column(db.String(100))