from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False) 
    password = db.Column(db.LargeBinary, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    classes = db.relationship('Classes', backref='user', lazy=True)

class Classes(db.Model):
    __tablename__ = 'classes'
    class_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    class_course_code = db.Column(db.String(100), nullable=False)
    class_section_number = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    created_at = db.Column(db.Date, default=datetime.today, nullable=False)
    expired_at = db.Column(db.Date, nullable=True)


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
    completion_status = db.Column(db.Boolean, default=False) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    user = db.relationship('User', backref=db.backref('assigned_courses', lazy=True))
    course = db.relationship('Courses', backref=db.backref('assigned_students', lazy=True))


class Courses(db.Model):
    _tablename__ = 'courses'

    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100))
    course_desc = db.Column(db.String(1000))
    section_number = db.Column(db.Float)
    level = db.Column(db.String(50))
    certificate = db.Column(db.Boolean, default=False)
    length = db.Column(db.String(20))
    route = db.Column(db.String(100))

class CourseSubsections(db.Model):
    __tablename__ = 'course_subsections'

    course_subsection_id = db.Column(db.Integer, primary_key=True)
    course_subsection_number = db.Column(db.Float)
    course_subsection_name = db.Column(db.String(100))

class StudentAssignedCourseSubsections(db.Model):
    __tablename__ = 'student_assigned_course_subsections'
        
    assigned_course_subsection_id = db.Column(db.Integer, primary_key=True)
    completion_status = db.Column(db.Boolean, default=False) 
    course_subsection_number = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    user = db.relationship('User', backref=db.backref('assigned_course_subsectons', lazy=True))

class Roles(db.Model):
    __tablename__ = "roles"

    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(100), nullable=False)
    role_desc = db.Column(db.String(1000))
    permission_id = db.Column(db.Integer)

    users = db.relationship('User', backref='role', lazy=True)

class StudentGrades(db.Model):
    __tablename__ = 'student_grades'
    student_grades_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    percentage_grade = db.Column(db.Float, nullable=False)
    course_subsection_id = db.Column(db.Integer, db.ForeignKey('course_subsections.course_subsection_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship('User', backref='grades')
    subsection = db.relationship('CourseSubsections', backref='grades')

class UserCodeLogs(db.Model):
    __tablename__ = 'user_code_logs'
    
    user_log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(50000))
    error = db.Column(db.String(10000))
    hints = db.Column(db.String(10000))
    page_context = db.Column(db.String(10000))
    static_issues = db.Column(db.String(10000))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    user = db.relationship('User', backref='logs')

class UserTimeLogs(db.Model):
    __tablename__ = 'user_time_logs'
    
    time_log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    page_context = db.Column(db.String(1000))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    duration = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    user = db.relationship('User', backref=db.backref('time_logs', lazy=True))

class UserPoints(db.Model):
    __tablename__ = 'user_points'
    
    user_points_id = db.Column(db.Integer, primary_key=True)
    num_points = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    user = db.relationship('User', backref=db.backref('points', lazy=True))