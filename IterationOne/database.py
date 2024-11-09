import psycopg
import bcrypt
import string
from classes import User

def check_default_values(new_user, default_firstname, default_lastname, default_email, default_username, default_password):
    # Check if any of the user's attributes match the default values
    if (new_user.firstname == default_firstname or
        new_user.lastname == default_lastname or
        new_user.email == default_email or
        new_user.username == default_username or
        new_user.password == default_password):
        print("Warning: One or more fields have default values.")
        return -1
    return 0

#Hashes the Password
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

#Checks if the plain text password matches the hashed password
def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def check_unique(cursor, username, email):
    cursor.execute("SELECT 1 FROM users WHERE username = %s OR email = %s;", (username, email))
    if cursor.fetchone() is None:
        return True
    else:
        return False

#Stores user in DB
def create_user(cursor, new_user):
    cursor.execute(
        '''
        INSERT INTO users (first_name, last_name, username, password_key, email, secret_key, user_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        ''',
        (new_user.firstname, new_user.lastname, new_user.username, new_user.password, new_user.email, new_user.secret_key, new_user.user_type)
    )
    cursor.connection.commit()

def check_password_requirements(password):
    min_length = 8
    has_length = False
    has_digit = False
    has_special_char = False
    has_upper = False
    if (len(password) >= min_length):
        has_length = True
    for char in password:
        if char.isupper():
            has_upper = True
        if char.isdigit():
            has_digit = True
        if char in string.punctuation:
            has_special_char = True

    if not has_length:
        print("Password needs a minimum of 8 characters.")

    if not has_upper:
        print("Password must contain at least one uppercase letter.")
    
    if not has_digit:
        print("Password must contain at least one number.")

    if not has_special_char:
        print("Password must contain at least one special character.")

    if has_length and has_upper and has_digit and has_special_char:
        return True  # Password meets all requirements
    else:
        return False

#User Schema is user_id (Primary Key), first_name, last_name, username (Unique), password_key, secret_key, email (Unique), user_type

def main():
    #Default Values to Be Referenced Later as a Checking Mechanism
    default_username = "defaultUsername"
    default_email = "defaultEmail"
    default_firstname = "defaultFirst"
    default_lastname = "defaultLast"
    default_password = "defaultPassword"

    new_user = User()

    first_name = input("Please enter your first name: ")
    last_name = input("Please enter your last name: ")
    email_address = input("Please enter your email: ")
    username = input("Please enter your username: ")

    while True:
        password = input("Please enter your password: ")
        if (check_password_requirements(password)):
            print("Password is valid.")
            break 
        else:
            print("Please try again.")

    new_user.firstname = first_name
    new_user.lastname = last_name
    new_user.email = email_address
    new_user.username = username
    new_user.password = password

    connection = psycopg.connect("dbname=test user=testuser password=testPassword host=localhost port=5432")
    cursor = connection.cursor()

    #Checks if the user failed to input a value when trying to create a new user
    if (check_default_values(new_user, default_firstname, default_lastname, default_email, default_username, default_password) == 0):
        #Hashes the password and creates the user
        new_user.password = hash_password(password)
        create_user(cursor, new_user)

main()

