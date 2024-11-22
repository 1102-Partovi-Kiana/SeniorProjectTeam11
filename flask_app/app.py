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
import jedi
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from config import Config
from auth_func import *
from classes import db, User


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
app.secret_key = 'secret-key-for-session'

CUSTOM_KEYWORDS = [
    "def", "class", "import", "while", "for", "if", "else", "elif", "try", "except", "finally", "with",
    "return", "print", "len", "range", "input", "open", "type", "isinstance", "id", "dir", "sorted",
    "enumerate", "zip", "map", "filter", "sum", "min", "max", "np.array", "np.linalg.norm", "np.append",
    "env.get_ball_position", "env.get_gripper_position", "env.step"
]

env = None  # Initialize your environment here


# Quiz data
quiz = {
    "questions": {
        "easy": [
            {
                "question": "What is a robot?",
                "options": [
                    "A machine that looks like a human",
                    "An embodied agent capable of sensing and decision-making",
                    "A tool used only in manufacturing",
                    "An AI system without physical form"
                ],
                "answer": 1
            },
            {
                "question": "What is the main purpose of robotics?",
                "options": [
                    "To build machines that can sense and interact with their environment",
                    "To entertain people",
                    "To replace human jobs",
                    "To make machines that look like humans"
                ],
                "answer": 1
            },
            {
                "question": "What are the three main functions typically performed by robots?",
                "options": [
                    "Sense, Compute, Act",
                    "Build, Program, Learn",
                    "Move, Interact, Process",
                    "Detect, React, Develop"
                ],
                "answer": 0
            },
            {
                "question": "What are collaborative robots (cobots) designed to do?",
                "options": [
                    "Work safely with humans",
                    "Use sensors to detect and interact with humans",
                    "Help with tasks like teamwork",
                    "Perform tasks without human involvement"
                ],
                "answer": 3
            },
            {
                "question": "In which industry are industrial robots most commonly used?",
                "options": [
                    "Healthcare",
                    "Manufacturing",
                    "Exploration",
                    "Entertainment"
                ],
                "answer": 1
            },
            {
                "question": "Which of the following disciplines does NOT play a core role in robotics?",
                "options": [
                    "Electrical Engineering",
                    "Mechanical Engineering",
                    "Computer Science",
                    "Linguistics"
                ],
                "answer": 3
            },
            {
                "question": "Which type of robot is designed to resemble and interact like humans?",
                "options": [
                    "Mobile Robots",
                    "Industrial Robots",
                    "Humanoid Robots",
                    "Collaborative Robots"
                ],
                "answer": 2
            },
            {
                "question": "Which of these is an example of where robots are commonly used?",
                "options": [
                    "Teaching students in a classroom",
                    "Performing surgeries in hospitals",
                    "Reading books to children",
                    "Walking pets in the park"
                ],
                "answer": 1
            },
            {
                "question": "What are agricultural robots (agribots) NOT designed to do?",
                "options": [
                    "Harvest and sort crops",
                    "Build greenhouses",
                    "Planting and seeding",
                    "Design buildings"
                ],
                "answer": 3
            },
            {
                "question": "What is one benefit of using robots in manufacturing?",
                "options": [
                    "They require no programming",
                    "They replace all human workers",
                    "They never need maintenance or repairs",
                    "They work faster and with greater precision than humans"
                ],
                "answer": 3
            }
        ],
        "medium": [
            {
                "question": "What topics does robotics intertwine with?",
                "options": [
                    "Artificial Intelligence",
                    "Computer Vision",
                    "Quantum Mechanics",
                    "Applied Mathematics"
                ],
                "answer": 2
            },
            {
                "question": "Which category of robots is specifically designed to navigate and operate in various environments autonomously or with minimal human intervention?",
                "options": [
                    "Industrial Robots",
                    "Humanoid Robots",
                    "Mobile Robots",
                    "Collaborative Robots"
                ],
                "answer": 2
            },
            {
                "question": "In robotics, what does the term manipulator refer to?",
                "options": [
                    "The sensory system of a robot",
                    "The central processing unit",
                    "The robotic arm used for moving objects",
                    "The mobile base of a robot"
                ],
                "answer": 2
            },
            {
                "question": "Which of these is an example of a collaborative robot (cobot)?",
                "options": [
                    "Atlas",
                    "UR5",
                    "Roomba",
                    "Unimate"
                ],
                "answer": 1
            },
            {
                "question": "Who coined the term 'robot'?",
                "options": [
                    "Isaac Asimov",
                    "Karel Čapek",
                    "George Devol",
                    "Ada Lovelace"
                ],
                "answer": 1
            },
            {
                "question": "Which invention by Charles Babbage helped influence robotics?",
                "options": [
                    "Analytical Engine",
                    "Water Clock",
                    "Jacquard Loom",
                    "Difference Engine"
                ],
                "answer": 0
            },
            {
                "question": "Which task is commonly performed by industrial robots?",
                "options": [
                    "Painting cars",
                    "Playing chess",
                    "Walking on two legs",
                    "Making medical diagnoses"
                ],
                "answer": 0
            },
            {
                "question": "Which invention by Joseph Jacquard in 1801 significantly influenced the development of programmable machines?",
                "options": [
                    "Water clock (Clepsydra)",
                    "Analytical Engine",
                    "Jacquard Loom",
                    "Flute player automaton"
                ],
                "answer": 2
            },
            {
                "question": "Which of these robots was designed for minimally invasive surgeries?",
                "options": [
                    "PR2",
                    "Da Vinci Surgical System",
                    "Unimate",
                    "Sophia"
                ],
                "answer": 1
            },
            {
                "question": "Which robot developed by Stanford University could reason about its environment?",
                "options": [
                    "Shakey",
                    "PR2",
                    "Spot",
                    "Da Vinci Surgical System"
                ],
                "answer": 0
            }
        ],
        "hard": [
            {
                "question": "Which robotics company developed robots like Atlas, Spot, and Handle?",
                "options": [
                    "Boston Dynamics",
                    "Universal Robots",
                    "Hanson Robotics",
                    "Willow Garage"
                ],
                "answer": 0
            },
            {
                "question": "What significant advancement in robotics was demonstrated by the Mars rovers such as Curiosity and Perseverance?",
                "options": [
                    "Development of humanoid mobility",
                    "Autonomous navigation and scientific data collection in extreme environments",
                    "Enhanced human-robot interaction capabilities",
                    "Implementation of soft robotics materials"
                ],
                "answer": 1
            },
            {
                "question": "What is a primary way in which animatronics and humanoid robots blur the lines between technology and entertainment in theme parks?",
                "options": [
                    "By performing repetitive tasks without interaction.",
                    "By entertaining, educating, and creating immersive experiences for visitors, blurring the boundaries between technology and entertainment.",
                    "By limiting their roles to backstage operations.",
                    "By focusing solely on mechanical movements without narrative elements."
                ],
                "answer": 1
            },
            {
                "question": "What key feature differentiates autonomous robots from other types of robots?",
                "options": [
                    "Ability to manipulate objects",
                    "Capability to make decisions without human intervention",
                    "Designed to resemble humans",
                    "Equipped with multiple axes of motion"
                ],
                "answer": 1
            },
            {
                "question": "Which of the following robotic systems integrates machine learning and artificial intelligence to adapt and make intelligent decisions based on environmental data?",
                "options": [
                    "Unimate",
                    "PR2",
                    "Da Vinci Surgical System",
                    "Sophia"
                ],
                "answer": 3
            },
            {
                "question": "How have collaborative robots (cobots) transformed human-robot collaboration in industrial settings compared to traditional industrial robots?",
                "options": [
                    "Cobots require extensive safety barriers, limiting interaction with humans",
                    "Cobots are designed to operate independently without human intervention",
                    "Cobots can safely work alongside humans, enhancing flexibility and productivity",
                    "Cobots are exclusively used for hazardous tasks, away from human workers."
                ],
                "answer": 2
            },
            {
                "question": "Which material is primarily used in soft robotics?",
                "options": [
                    "Metal",
                    "Elastomers",
                    "Carbon Fiber",
                    "Plastic"
                ],
                "answer": 1
            },
            {
                "question": "What is a collaborative robot (cobot) primarily designed to do?",
                "options": [
                    "Operate autonomously in hazardous environments",
                    "Work safely alongside humans in a shared workspace",
                    "Replace human workers in factories",
                    "Navigate challenging terrains autonomously"
                ],
                "answer": 1
            },
            {
                "question": "Which robot was the first industrial robot used in manufacturing?",
                "options": [
                    "Da Vinci Surgical System",
                    "PR2",
                    "Unimate",
                    "Baxter"
                ],
                "answer": 2
            },
            {
                "question": "Which robot developed by Boston Dynamics is known for its humanoid agility?",
                "options": [
                    "Atlas",
                    "Spot",
                    "Shakey",
                    "Baxter"
                ],
                "answer": 0
            }
        ]
    }
}

# Route for the homepage
@app.route('/')
def RenderHomepage():
    return render_template('homepage.html')

@app.route('/get-suggestions', methods=['POST'])
def get_suggestions():
    data = request.json
    code = data.get('code', '')
    line = data.get('line', 0)
    column = data.get('column', 0)

    try:
        script = jedi.Script(code, line, column)
        jedi_suggestions = [completion.name for completion in script.complete()]
    except Exception as e:
        jedi_suggestions = []

    suggestions = list(set(CUSTOM_KEYWORDS + jedi_suggestions)) 
    suggestions.sort()  
    return jsonify(suggestions)

@app.route('/Chatbot')
def RenderChatbot():
    return render_template('chatbot.html')

attempt_counter = 0
user_submitted_code = ""
api_key = "AIzaSyDpL6NsK8v8alk8JPVmu9S1QF8oRNhCJDU"  

@app.route('/chatbot-api-2', methods=['POST'])
def ChatbotAPI2():
    print("Chatbot API 2 called")  
    user_message = request.json.get('message')
    page_context = request.json.get('page_context', "general") 
    print("Received user message:", user_message)
    print("Page context:", page_context)

    general_prompts = {
        "Homepage": "You are a helpful chatbot for the homepage of a robotics education platform. Provide an overview of features, navigation tips, and highlight key sections of the platform.",
        "Contact": "You are a helpful chatbot for the contact page. Assist users with information on how to reach out for support, provide email or phone details, or guide them to submit a query through the contact form.",
        "Courses": "You are a helpful chatbot for the courses page. Provide information about available robotics courses, their descriptions, and how to enroll or access them.",
        "General": "You are a general-purpose chatbot for a robotics education platform. Help users with their questions about the platform, navigating the site, or any robotics-related queries they might have."
    }

    prompt = general_prompts.get(page_context, general_prompts["General"])

    full_prompt = f"""
    {prompt}

    User Message: {user_message}
    Respond concisely and helpfully. If the question is unclear, ask for clarification.
    """

    api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": full_prompt
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(f"{api_url}?key={api_key}", headers={
            'Content-Type': 'application/json'
        }, json=payload)

        if response.status_code == 200:
            response_json = response.json()
            chatbot_response = response_json.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', 'No response')
            return jsonify({'reply': chatbot_response})
        else:
            print("Error:", response.status_code, response.text)  
            return jsonify({'error': f"Error: {response.status_code}, {response.text}"}), response.status_code

    except Exception as e:
        print("Error occurred:", e)
        return jsonify({'error': str(e)}), 500



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

        if not check_password_requirements(password):
            return render_template('account/signup.html')
        
        new_user = User()

        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.email = email
        new_user.username = username
        new_user.password = hash_password(password)
        new_user.secret_key = "DefaultSecretKey"
        new_user.user_type = "DefaultUserType"

        if (check_default_values(new_user) == False):
            if User.query.filter_by(username=username).first():
                flash("Username is already taken.")
                return render_template('account/signup.html')
            if User.query.filter_by(email=email).first():
                flash("Email is already taken.")
                return render_template('account/signup.html')
            db.session.add(new_user)
            db.session.commit()
            flash("Registration Successful")
            return render_template('account/signup.html')

    return render_template('account/signup.html')

@app.route('/login', methods=['GET', 'POST'])
def RenderLogin():
    if request.method == 'POST':
        login_username = request.form.get('login_username')
        login_password = request.form.get('login_password')

        if(check_valid_user(login_username, login_password)):
            flash("Successfully Logged In!")

    return render_template('account/login.html')

@app.route('/courses')
def RenderCourses():
    return render_template('courses.html')

@app.route('/module1/introduction')
def module_intro():
    return render_template('courses/course1-content/module_intro.html') 

@app.route('/module1/introduction/overview')
def overview():
    return render_template('courses/course1-content/overview.html')

@app.route('/module1/introduction/history')
def history():
    return render_template('courses/course1-content/history_of_robotics.html')

@app.route('/module1/introduction/types-of-robots')
def typesofrobots():
    return render_template('courses/course1-content/types_of_robots.html')

@app.route('/module1/introduction/importance-and-applications-of-robotics')
def importanceandapp():
    return render_template('courses/course1-content/importance_and_app.html')

@app.route('/module1/introduction/course1-quiz-1')
def course1quiz1():
    return render_template('courses/course1-content/course1-quiz1.html')

@app.route('/module1/introduction/robot-anatomy')
def robotanatomy():
    return render_template('courses/course1-content/robot_anatomy.html')

@app.route('/module1/introduction/challenges')
def challenges():
    return render_template('courses/course1-content/challenges_in_robotics.html')

@app.route('/module1/introduction/robot-programming')
def robotprogramming():
    return render_template('courses/course1-content/robot_programming.html')

@app.route('/module1/introduction/social-and-ethical-implications')
def implications():
    return render_template('courses/course1-content/social_and_ethical_imp.html')

@app.route('/module1/introduction/future-trends')
def futuretrends():
    return render_template('courses/course1-content/future_trends.html')

@app.route('/module2/introduction')
def module_two():
    return render_template('courses/course2-content/module_two.html') 

@app.route('/module2/introduction/introduction-of-mobile-robots')
def intro_of_mobile_robots():
    return render_template('courses/course2-content/intro_of_mobile_robots.html')

@app.route('/module2/introduction/idustrial-robots')
def industrial_robots():
    return render_template('courses/course2-content/industrial_robots.html')

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
    global user_submitted_code
    code = request.form['code']
    user_submitted_code = code 
    
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

@app.route('/next-question', methods=['POST'])
def next_question():
    data = request.json

    # Extract state from the request
    questions_served = data.get('questions_served', 0)
    score = data.get('score', 0)
    difficulty = data.get('difficulty', 'easy')
    used_questions = data.get('used_questions', [])
    last_correct = data.get('last_correct', True)  # Indicates if the last answer was correct

    if questions_served >= 10:
        return jsonify({
            "message": "Quiz complete!",
            "done": True,
            "score": score
        })

    # Adjust difficulty based on the correctness of the last answer
    if questions_served > 0:
        if last_correct and difficulty == "easy":
            difficulty = "medium"
        elif last_correct and difficulty == "medium":
            difficulty = "hard"
        elif not last_correct and difficulty == "medium":
            difficulty = "easy"
        elif not last_correct and difficulty == "hard":
            difficulty = "medium"

    # Update score if the last answer was correct
    if last_correct:
        score += 1

    current_difficulty = difficulty
    available_questions = [
        q for q in quiz["questions"][current_difficulty]
        if q not in used_questions
    ]

    if not available_questions:
        if current_difficulty == "hard":
            current_difficulty = "medium"
        elif current_difficulty == "medium":
            current_difficulty = "easy"
        available_questions = [
            q for q in quiz["questions"][current_difficulty]
            if q not in used_questions
        ]

    if not available_questions:
        return jsonify({"message": "No more questions available!", "done": True, "score": score})

    question = random.choice(available_questions)
    used_questions.append(question)
    questions_served += 1

    return jsonify({
        "question": question,
        "difficulty": current_difficulty,
        "questions_served": questions_served,
        "score": score,
        "used_questions": used_questions,
        "done": False
    })

@app.route('/quiz1', methods=['GET'])
def render_quiz_page():
    # Render the quiz page with initial state handled on the client side
    return render_template('quiz1.html')

if __name__ == '__main__':
    app.run(debug=True)
