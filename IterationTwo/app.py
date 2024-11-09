from flask import Flask, render_template, request, flash, redirect, url_for
import psycopg
import bcrypt
import string
from classes import User
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

def check_default_values(new_user):
    default_username = "defaultUsername"
    default_email = "defaultEmail"
    default_firstname = "defaultFirst"
    default_lastname = "defaultLast"
    default_password = "defaultPassword"
    
    # Check if any of the user's attributes match the default values
    if (new_user.firstname == default_firstname or
        new_user.lastname == default_lastname or
        new_user.email == default_email or
        new_user.username == default_username or
        new_user.password == default_password):
        flash("Warning: One or more fields have no values.")
        return True
    return False

#Checks if the username is unique
def check_unique_username(cursor, username):
    cursor.execute(
        '''
        SELECT username FROM users WHERE username = %s
        ''', (username,)
    )
    result = cursor.fetchone()
    if result is not None:
        return False
    return True

#Checks if the email address is unique
def check_unique_email(cursor, email):
    cursor.execute(
        '''
        SELECT email FROM users WHERE email = %s
        ''', (email,)
    )
    result = cursor.fetchone()
    if result is not None:
        return False
    return True

#Hashes the Password
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

#Checks if the plain text password matches the hashed password
def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

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

#Checks if password follows a minimum of 8 charactesr with 1 digit and 1 special character and 1 uppercase letter
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
        flash("Password needs a minimum of 8 characters.")

    if not has_upper:
        flash("Password must contain at least one uppercase letter.")
    
    if not has_digit:
        flash("Password must contain at least one number.")

    if not has_special_char:
        flash("Password must contain at least one special character.")

    if has_length and has_upper and has_digit and has_special_char:
        return True  # Password meets all requirements
    else:
        return False

#Login Process Function which checks if the user exists within the database and that the password matches to login
def check_valid_user(cursor, login_username, login_password):
    cursor.execute(
        '''
        SELECT password_key FROM users WHERE username = %s
        '''
        , (login_username,)
    )
    result = cursor.fetchone()
    if result is None:
        print("Invalid Username")
        return False
    hashed_password = result[0]
    return check_password(login_password, hashed_password)



#All the Flask Stuff

# Define the route for the home page
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register_user():
    connection = psycopg.connect("dbname=test user=testuser password=testPassword host=localhost port=5432")
    cursor = connection.cursor()
    
    if request.method == 'POST':
        # Store input values in variables   
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

    if not check_password_requirements(password):
        return redirect(url_for('home'))
    
    new_user = User()

    new_user.firstname = first_name
    new_user.lastname = last_name
    new_user.email = email
    new_user.username = username
    new_user.password = password

    if (check_default_values(new_user) == False and check_unique_username() and check_unique_email):
        #Hashes the password and creates the user
        new_user.password = hash_password(password)
        create_user(cursor, new_user)

    cursor.close()
    connection.close()

    return redirect(url_for('home'))

@app.route('/login', methods=['POST'])
def login_user():
    connection = psycopg.connect("dbname=test user=testuser password=testPassword host=localhost port=5432")
    cursor = connection.cursor()
    if request.method == 'POST':
        login_username = request.form.get('login_username')
        login_password = request.form.get('login_password')
    
    if(check_valid_user(cursor, login_username, login_password)):
        print("Successfully Logged In!")

    cursor.close()
    connection.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

