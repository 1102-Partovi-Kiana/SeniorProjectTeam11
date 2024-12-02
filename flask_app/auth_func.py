from flask import flash
import bcrypt
import string
import secrets
from classes import *
import re

# Check if the new user's attributes have default values
def check_default_values(new_user):
    default_username = "defaultUsername"
    default_email = "defaultEmail"
    default_firstname = "defaultFirst"
    default_lastname = "defaultLast"
    default_password = "defaultPassword"
    
    if (new_user.first_name == default_firstname or
        new_user.last_name == default_lastname or
        new_user.email == default_email or
        new_user.username == default_username or
        new_user.password == default_password):
        flash("Warning: One or more fields have no values.")
        return True
    return False

# Hashes the password
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

# Checks if the plain-text password matches the hashed password
def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

# Checks if password meets the minimum requirements
def check_password_requirements(password):
    min_length = 8
    has_length = len(password) >= min_length
    has_upper = any(char.isupper() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special_char = any(char in string.punctuation for char in password)

    if not has_length:
        flash("Password needs a minimum of 8 characters.")
    if not has_upper:
        flash("Password must contain at least one uppercase letter.")
    if not has_digit:
        flash("Password must contain at least one number.")
    if not has_special_char:
        flash("Password must contain at least one special character.")

    return has_length and has_upper and has_digit and has_special_char

# Checks if a username and password combination is valid
def get_user(login_username):
    user = User.query.filter_by(username=login_username).first()
    if user is not None:
        return True, user
    #flash("Invalid Username")
    return False, None

def check_login_info(user, login_password):
    return bcrypt.checkpw(login_password.encode('utf-8'), user.password)

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com|org|net|edu|gov)$'
    return bool(re.match(pattern, email))

def is_valid_course_code(course_code):
    pattern = r'^[A-Za-z]+\d+$'
    return bool(re.match(pattern, course_code))

def get_classes(user_id):
    classes = Classes.query.filter_by(user_id = user_id).all()
    if (classes is None):
        print("No classes returned")
        return None
    return classes

def generate_class_code():
    length = 8
    characters = string.ascii_letters + string.digits
    while True:
        class_code = ''.join(secrets.choice(characters) for _ in range(length))
        existing_code = ClassCodes.query.filter_by(class_code = class_code).first()
        if (existing_code is None):
            return class_code