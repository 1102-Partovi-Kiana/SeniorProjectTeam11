from flask import Flask, render_template, request, jsonify, Response, flash, redirect, url_for, session
import mujoco_py
import numpy as np
import cv2  # Import OpenCV
from reach import ReachEnv  # Ensure this imports your ReachEnv class
from pickandplace import FetchPickAndPlaceEnv
from organize import FetchOrganizeEnv
from stack import FetchStackEnv
import requests  # Import requests library for API communication
import random
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from config import Config
from auth_func import *
from email_func import *
from classes import *


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
mail.init_app(app)


env = None  # Initialize your environment here

# Route for the homepage
@app.route('/')
def RenderHomepage():
    return render_template('homepage.html', is_homepage=True)

@app.route('/robotic-environment')
def RenderRoboticEnvironment():
    return render_template('robotic_environment.html')

@app.route('/Chatbot')
def RenderChatbot():
    return render_template('chatbot.html')

attempt_counter = 0
user_submitted_code = ""
api_key = "AIzaSyDpL6NsK8v8alk8JPVmu9S1QF8oRNhCJDU"  
@app.route('/chatbot-api', methods=['POST'])
def ChatbotAPI():
    print("Chatbot API called")  # Check if the function is called
    global attempt_counter, user_submitted_code
    user_message = request.json.get('message')
    print("Received user message:", user_message) 
    print("User submitted code in ChatbotAPI:", user_submitted_code)

    robot_jokes = [
        "Why did the robot cross the road? To recharge on the other side!",
        "What do you call a robot who always runs late? A bit slow in processing!",
        "How do robots pay for things? With cache!",
        "Why was the robot so bad at soccer? Because it kept kicking up errors!",
        "What’s a robot’s favorite genre of music? Heavy metal!",
        "Why did the robot go on a diet? It had too many bytes!",
    ]

    # Defining common acknowledgment phrases
    acknowledgment_phrases = [
    "ok cool", "thank you", "thanks", "sounds good", "great", "awesome", 
    "nice", "alright", "got it", "understood", "makes sense", "perfect", 
    "cool", "okay", "all set", "roger that", "good to know", "fine", 
    "will do", "no problem", "much appreciated", "I see", "noted", "gotcha"
    ]

    long_acknowledgment_phrases = [
    "That makes a lot of sense, thank you!", 
    "Got it, I appreciate the help!", 
    "Perfect, that's exactly what I needed to know.", 
    "Thanks for clarifying that!", 
    "Alright, that really clears things up, thanks!",
    "Thanks a bunch! That explanation was super helpful.", 
    "Awesome, thanks for pointing me in the right direction!", 
    "Okay, that answers my question perfectly.", 
    "Great, I feel much more confident about this now.", 
    "Excellent, that was the info I was looking for!", 
    "Got it, that’s really helpful, thanks!", 
    "Thank you, I think I’m on the right track now.", 
    "Cool, I think I understand it fully now!", 
    "Awesome, you really made it easy to understand!", 
    "This is exactly what I needed, thank you so much!", 
    "Thanks, now I can move forward with confidence!", 
    "Alright, that totally makes sense, appreciate it!", 
    "Gotcha, thanks for helping me figure this out!", 
    "Perfect, that explanation really helped a lot!", 
    "Thank you! That was really helpful and clear.", 
    "Got it, this is really helpful guidance, thank you.", 
    "Thanks for helping me wrap my head around this!", 
    "Nice, that clarifies everything for me. Thanks!", 
    "Much appreciated, this is really helpful information.", 
    "Alright, I think I’m all set now. Thanks a ton!"
    ]

    random_joke = random.choice(robot_jokes)
    if attempt_counter == 0 and user_submitted_code == "":
        welcome_message = (
            f"Hi there! I'm your friendly coding assistant, ready to help you with your project. 😊\n\n"
            f"Here's a robot joke to get started: {random_joke}\n\n"
            "Feel free to submit your code or ask any questions about your coding challenges!"
        )
        attempt_counter += 1  # Increment attempt counter to avoid repeating the welcome message
        return jsonify({'reply': welcome_message})

    all_acknowledgment_phrases = acknowledgment_phrases + long_acknowledgment_phrases

    if not user_submitted_code:
        return jsonify({'reply': "Please submit your code before asking for help!"})
    
    # If the user message contains an acknowledgment, respond accordingly
    if any(phrase in user_message.lower() for phrase in all_acknowledgment_phrases):
        return jsonify({'reply': "I'm glad to hear that! Let me know if you have more questions or need further assistance."})

    # Construct prompt using stored code
    prompt = f"""

    You are a helpful chatbot for a robotics coding environment. If the user's message contains acknowledgment or expressions like "thanks," "got it," "okay," or other similar acknowledgment phrases, respond with a friendly encouragement or acknowledgment without giving any hint or solution. 
    Otherwise, analyze the following Python code intended to make a robotic gripper move towards a ball. Identify any potential issues in the logic and provide specific hints for improvement.

    User Code:
    {user_submitted_code}

    Problem Context: This code is supposed to move the gripper towards the ball until it reaches a close range. Key factors include:
    - Ensuring the distance threshold is set low enough for the gripper to stop close to the ball.
    - Verifying the direction vector is normalized to ensure the gripper moves towards the ball consistently.

    A general solution to the environment is 
        ball_position = current_env.get_ball_position()
        gripper_position = current_env.get_gripper_position()
        direction = np.array(ball_position) - np.array(gripper_position)
        distance_threshold = 0.01
        step_size = 0.05
        while np.linalg.norm(direction) > distance_threshold:
            action = np.append(direction / np.linalg.norm(direction) * step_size, [1])
            current_env.step(action)
            gripper_position = current_env.get_gripper_position()
            direction = np.array(ball_position) - np.array(gripper_position)

        print("Final Gripper Position:", gripper_position)
        print("Reached near the ball.")

    User's Question: {user_message}
    """

    # Increment the attempt counter
    attempt_counter += 1
    print(f"Attempt Counter (after increment): {attempt_counter}")  # Confirm counter increment

    # API call to Gemini for chatbot response
    try:
        api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }
        
        response = requests.post(f"{api_url}?key={api_key}", headers={
            'Content-Type': 'application/json'
        }, json=payload)
        
        print("API Response:", response.text)  # Debugging API response

        if response.status_code != 200:
            return jsonify({'error': f'Error from API: {response.text}'}), 500

        response_json = response.json()

        # Extract the response from the API
        if 'candidates' in response_json and len(response_json['candidates']) > 0:
            chatbot_response = response_json['candidates'][0]['content']['parts'][0].get('text', 'No response')
            print("Extracted Chatbot Response:", chatbot_response)  # Debug chatbot response
        else:
            chatbot_response = 'No contents available in the response'

    except Exception as e:
        print("Error occurred:", e)
        return jsonify({'error': str(e)}), 500

    # Apply the hint and solution logic based on the attempt count
    if attempt_counter < 4:
        hint = "Hint: Try checking the distance threshold to ensure the gripper reaches close enough to the ball."
        final_response = f"{chatbot_response}\n\n{hint}"
        print("Final Response with Hint:", final_response)  # Confirm response with hint
        return jsonify({'reply': final_response})
    else:
        # Provide solution after 3 attempts and reset counter
        solution = """Here’s how to solve it:
            ball_position = current_env.get_ball_position()
            gripper_position = current_env.get_gripper_position()
            direction = np.array(ball_position) - np.array(gripper_position)
            distance_threshold = 0.01
            step_size = 0.05
            while np.linalg.norm(direction) > distance_threshold:
                action = np.append(direction / np.linalg.norm(direction) * step_size, [1])
                current_env.step(action)
                gripper_position = current_env.get_gripper_position()
                direction = np.array(ball_position) - np.array(gripper_position)

            print("Final Gripper Position:", gripper_position)
            print("Reached near the ball.")
        """
        attempt_counter = 0  # Reset the counter after giving the solution
        final_response = f"{chatbot_response}\n\n{solution}"
        print("Final Response with Solution:", final_response)  # Confirm response with solution
        return jsonify({'reply': final_response})


@app.route('/environments')
def RenderEnvironmentList():
    environments = [
        # Example list of environment data
        {
            'id': 1,
            'name': 'FetchPickAndPlace-v1',
            'brief_description': 'Move the box to the floating goal position.',
            'preview_filename': 'fetchpickandplace.mp4'
        },
        # Add more environments as needed
    ]
    return render_template('environments-landing.html', environments=environments)

@app.route('/environment/<int:environment_id>')
def RenderEnvironment(environment_id):
    environments = [
        {
            'id': 1,
            'name': 'FetchPickAndPlace-v1',
            'brief_description': 'Move the box to the floating goal position.',
            'preview_filename': 'fetchpickandplace.mp4'
        },
        # Add more environments as needed
    ]
    
    environment = next((env for env in environments if env['id'] == environment_id), None)
    
    if environment is None:
        return "Environment not found", 404

    return render_template('environment_detail.html', environment=environment)

@app.route('/signup', methods=['GET', 'POST'])
def RenderSignup():
    if request.method == 'POST':
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        account_type = request.form.get('account_type')

        if (not check_password_requirements(password)):
            return render_template('account/signup.html', is_homepage=True)
        
        if (not is_valid_email(email)):
            flash("Invalid Email Address")
            return render_template('account/signup.html', is_homepage=True)

        new_user = User()

        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.email = email
        new_user.username = username
        new_user.password = hash_password(password)
        if (account_type == 'instructor'):
            new_user.role_id = 1
        elif (account_type == 'student'):
            new_user.role_id = 2

        if (check_default_values(new_user) == False):
            if User.query.filter_by(username=username).first():
                flash("Username is already taken.")
                return render_template('account/signup.html')
            if User.query.filter_by(email=email).first():
                flash("Email is already taken.")
                return render_template('account/signup.html')
            if password != confirm_password:
                flash("Password does not match.")
                return render_template('account/signup.html')
            db.session.add(new_user)
            db.session.commit() 
            flash("Registration Successful")
            if (new_user.role_id == 1):
                return redirect(url_for('RenderInstructorDashboard'))
            elif(new_user.role_id == 2):
                return redirect(url_for('RenderStudentDashboard'))

    return render_template('account/signup.html', is_homepage=True)

@app.route('/login', methods=['GET', 'POST'])
def RenderLogin():
    if request.method == 'POST':
        login_username = request.form.get('login_username')
        login_password = request.form.get('login_password')

        success, user = get_user(login_username)
        if (success):
            if(check_login_info(user, login_password)):
                flash('Login Successful')
                session['user_id'] = user.user_id
                role = get_user_role(user)
                if (role == 1):
                    return redirect(url_for('RenderInstructorDashboard'))
                elif (role == 2):
                    return redirect(url_for('RenderStudentDashboard'))
            else:
                flash('Invalid Password')
    session.pop('_flashes', None)
    return render_template('account/login.html', is_homepage=True)

@app.route('/forgot-password', methods=['GET', 'POST'])
def RenderForgotPassword():
    if request.method == 'POST':
        username = request.form.get('login_username')
        success, user = get_user(username)
        if (success):
            print(f"Received username for password reset: {username}")
            flash("An email been sent to your account.", "success")
            subject = "CORE - Reset Password"
            email = "officialwarerecovery@gmail.com"
            password_reset_link = "http://127.0.0.1:5000/reset-password"
            #Instead of manually reading the file, we are taking advantage of Flask's Jinja2 templating
            body = render_template("account/forgot_password.txt", username = username, password_reset_link = password_reset_link)
            send_email(subject, email, body)
        return redirect(url_for('RenderForgotPassword'))
    return render_template('account/forgot_password.html')

@app.route('/reset-password', methods=['GET', 'POST'])
def RenderResetPassword():
    if request.method == 'POST':
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')
        if new_password == confirm_password:
            flash("Password has been reset successfully.", "success")
        else:
            flash("Passwords do not match.", "error")
        return redirect(url_for('reset_password'))
    return render_template('account/reset_password.html')

@app.route('/dashboard/instructor_view', methods=['GET', 'POST'])
def RenderInstructorDashboard():
    user_id = session.get('user_id')
    if not user_id:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))
    if request.method == 'POST':
        class_course_code = request.form['classCourseCode']
        class_section = request.form['classSection']
        class_date = request.form['classDate']

        new_class = Classes()
        new_class.class_course_code = class_course_code
        new_class.class_section_number = class_section
        new_class.user_id = user_id
        db.session.add(new_class)
        db.session.commit() 
        return redirect(url_for('RenderInstructorDashboard'))
    return render_template('dashboard/dashboard_instructor.html', is_dashboard=True, is_instructor_dashboard=True)

@app.route('/dashboard/student_view', methods=['GET'])
def RenderStudentDashboard():
    return render_template('dashboard/dashboard_student.html', is_dashboard=True, is_student_dashboard=True)

@app.route('/courses')
def RenderCourses():
    return render_template('courses.html')

@app.route('/module1/introduction')
def module_intro():
    return render_template('course1-content/module_intro.html') 

@app.route('/module1/introduction/overview')
def overview():
    return render_template('course1-content/overview.html')

@app.route('/module1/introduction/history')
def history():
    return render_template('course1-content/history_of_robotics.html')

@app.route('/module1/introduction/typesofrobots')
def typesofrobots():
    return render_template('course1-content/types_of_robots.html')

@app.route('/module1/introduction/importanceandapplicationsofrobotics')
def importanceandapp():
    return render_template('course1-content/importance_and_app.html')

@app.route('/module1/introduction/robotanatomy')
def robotanatomy():
    return render_template('course1-content/robot_anatomy.html')

@app.route('/DarrenPage')
def RenderDarrenEnv():
    global env
    env = ReachEnv()
    return render_template('robotic_environment.html')

@app.route('/PickAndPlacePage')
def RenderPickAndPlaceEnv():
    global env
    env = FetchPickAndPlaceEnv()
    return render_template('robotic_pick_and_place_environment.html')

@app.route('/FetchStackPage')
def RenderFetchStackEnv():
    global env
    env = FetchStackEnv()
    return render_template('fetch_stack_environment.html')


@app.route('/FetchOrganizePage')
def RenderFetchOrganizeEnv():
    global env
    env = FetchOrganizeEnv()
    return render_template('robotic_organize_environment.html')

def generate_frames():
    global env  # Access the global environment instance
    while True:
        frame = env.render(mode='rgb_array', width=1440, height=1080)
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/run-code', methods=['POST'])
def run_code():
    code = request.form['code']
    
    if env is None:
        return jsonify({'error': 'No environment selected'}), 400
    
    try:
        local_context = {}
        exec(code, globals(), local_context)

        ball_position = local_context.get('ball_position', env.get_ball_position())
        gripper_position = local_context.get('gripper_position', env.get_gripper_position())
        #box_position = local_context.get('box_position', current_env.get_box_position())

        return jsonify({
            'message': 'Code executed successfully.',
            'ball_position': {'x': ball_position[0], 'y': ball_position[1], 'z': ball_position[2]},
            'gripper_position': {'x': gripper_position[0], 'y': gripper_position[1], 'z': gripper_position[2]},
            #'box_position': {'x': box_position[0], 'y': box_position[1], 'z': box_position[2]},
            'error': None,
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
        })

@app.route('/get-ball-position', methods=['GET'])
def get_ball_position():
    position = env.get_ball_position() 
    return jsonify({'x': position[0], 'y': position[1], 'z': position[2]})

@app.route('/get-gripper-position', methods=['GET'])
def get_gripper_position():
    position = env.get_gripper_position()  
    return jsonify({'x': position[0], 'y': position[1], 'z': position[2]})

@app.route('/get-box-position', methods=['GET'])
def get_box_position():
    position = env.get_box_position() 
    return jsonify({'x': position[0], 'y': position[1], 'z': position[2]})

@app.route('/check-collision', methods=['GET'])
def check_collision():
    ball_position = env.get_ball_position()
    gripper_position = env.get_gripper_position()
    # box_position = current_env.get_box_position()
    
    threshold_distance = 0.01 
    distance = np.linalg.norm(np.array(ball_position) - np.array(gripper_position))

    collision_detected = bool(distance < threshold_distance)
    return jsonify({'collision': collision_detected})

if __name__ == '__main__':
    app.run(debug=True)
