from flask import Flask, render_template, request, jsonify, Response, flash, redirect, url_for, session
import mujoco_py
import numpy as np
import cv2 
from reach import ReachEnv 
from pickandplace import FetchPickAndPlaceEnv
from organize import FetchOrganizeEnv
from stack import FetchStackEnv
from organize_sensors import FetchOrganizeSensorsEnv
from car import CarEnv
import requests
import random
import jedi
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from flask_mail import Mail, Message
from config import Config
from email_func import *
from classes import *
from auth_func import *
import time
import glfw
import threading
import gymnasium as gym
import ast

app = Flask(__name__, static_folder='static')
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
mail.init_app(app)

ROLE_INSTRUCTOR = 1
ROLE_STUDENT = 2

CUSTOM_KEYWORDS = [
    "def", "class", "import", "while", "for", "if", "else", "elif", "try", "except", "finally", "with",
    "return", "print", "len", "range", "input", "open", "type", "isinstance", "id", "dir", "sorted",
    "enumerate", "zip", "map", "filter", "sum", "min", "max", "abs", "np.array", "np.linalg.norm", 
    "np.append", "np.subtract", "np.add", "np.divide", "np.multiply", "np.zeros", "np.ones", "np.dot",
    "env.sim.data.get_site_xpos", "env.sim.model.geom_name2id", "env.sim.model.geom_rgba",
    "env.sim", "env.step", "env.reset", "env.render", "env.action_space", "env.observation_space", 
    "env.get_ball_position", "env.get_gripper_position", "env.get_sensor_forward_value", 
    "env.get_sensor_right_value", "env.get_sensor_left_value", "env.get_sensor_backward_value", 
    "SENSOR_THRESHOLD", "distance_threshold", "box_to_ball_threshold", "close_grip_action", 
    "open_grip_action", "lift_action", "horizontal_action", "descend_action", "move_to_ball_action", 
    "ascend_action", "return_to_previous_action", "horizontal_distance", "vertical_distance", 
    "distance_to_ball", "distance_to_box", "distance_to_previous", "direction", "direction_normalized", 
    "direction_to_ball", "direction_to_container", "direction_to_previous", "gripper_position", 
    "box_position", "ball_position", "container_position", "previous_gripper_position", "color", 
    "target_color", "geom_id", "rgba", "np.array_equal", "num_steps", "break", "handle_object", 
    "object_name", "'object0'", "'object1'", "'object2'", "'object3'", "forward", "right", "left", 
    "backward", "values", "greatest_direction", "greatest_value", "action", 
    "[0.005, 0.007]", "[0.005, -0.007]", "[0.01, 0.0]", "max", "time.sleep", 
    '"Forward"', '"Right"', '"Left"'
]

env = None 

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
    return render_template('homepage.html', is_homepage=True)

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

def check_normalization(tree):
    """Check if the direction vector is normalized."""
    issues = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            if isinstance(node.value, ast.BinOp) and "normalize" not in ast.dump(node.value):
                issues.append("Direction vector might not be normalized.")
    return issues

def check_distance_threshold(tree):
    """Check if the distance_threshold is used in the while loop condition."""
    issues = []
    for node in ast.walk(tree):
        if isinstance(node, ast.While):
            if not any(
                isinstance(condition, ast.Compare) and "distance_threshold" in ast.dump(condition)
                for condition in ast.walk(node.test)
            ):
                issues.append("While loop does not use distance_threshold for termination.")
    return issues

def check_gripper_closure(tree):
    """Check if the gripper closes at the correct time."""
    issues = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if hasattr(node.func, "id") and node.func.id == "close_gripper":
                if not hasattr(node, "gripper_reached_object"):
                    issues.append("Gripper might not close after reaching the object.")
    return issues

def check_object_transport(tree):
    """Check if the object is transported to the target position."""
    issues = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if hasattr(node.func, "id") and node.func.id == "move_gripper":
                if not hasattr(node, "target_position"):
                    issues.append("Gripper might not move the object to the target position.")
    return issues

@app.route('/Chatbot')
def RenderChatbot():
    return render_template('chatbot.html')

attempt_counter = 0
user_submitted_code = ""
last_error = None
static_issues = []
junk_array = []
api_key = "AIzaSyDpL6NsK8v8alk8JPVmu9S1QF8oRNhCJDU"  

@app.route('/chatbot-api-2', methods=['POST'])
def ChatbotAPI2():
    print("Chatbot API 2 called")  
    user_message = request.json.get('message')
    page_context = request.json.get('page_context', "General") 
    print("Received user message:", user_message)
    print("Page context:", page_context)

    general_prompts = {
        "Homepage": """Your name is Cora. I am providing you your name for your own context, don't bring it up in every response to the user.
                       You are a helpful chatbot for the homepage of a robotics education platform for undergraduates. 
                       The platforms name is CORE, which stands for Centers for Optimizing Robotics Education. 
                       I am providing you the name of the platform for your own context, don't bring it up in every response to the user, except for your first response, 
                       where you are greeting the user to the platform. 
                       Provide an overview of features, what the purpose of the platforms is, and highlight key sections of the platform.
                       When responding, adhere strictly to the following details about the platform. These details are for usage, don't list them all out to the user in the format I have them written for you. 
                       Here they are:
                       ## Platform Features:
                        1. *Courses*: CORE offers robotics courses, such as Introduction to Robotics, Types of Robots, Fetch Robot, and more. Each course includes certificates upon completion and builds specific skills like coding, object manipulation, or self-driving car programming.
                        2. *Virtual Robotics Lab*: Students can code, simulate, and test robots in a user-friendly coding environment with features like:
                        - Code Editor with syntax highlighting and autocompletion.
                        - Simulation Viewer to visualize robotic actions in real-time.
                        - Coding Terminal for output results and debugging.
                        3. *Customizable Lab Settings*: Students can toggle dark/light mode, enable or disable coding pets, and personalize syntax highlighting.
                        4. *Hints and Assistance*: Students have access to personalized hints to help them in their coding tasks. 
                       ## Purpose of the Platform:
                        - CORE is designed to make robotics education accessible and interactive for undergraduates. 
                        - Core aspires to make the high learning curve of robotics less intimidating for undergraduates. 
                        - CORE aims to inspire and prepare the next generation of robotics engineers.
                        - CORE is a place where students can learn the principles of robotics without previous experience.
                        - CORE aspires to make robotics an engaging and accessible experience.

                        Here are some more notes: 
                        - If the user's question is unclear, ask for clarification politely.
                        - If the user tells you that they don't need any more help. Tell them a very kind message back, and mention how your awlays here for any future 
                        questions that may come up. 
                        - If the user tells you something along the lines of "Great thank you for your help!" or "Thank you", they don't need any more help. Tell them a very kind message back, and mention how your awlays here for any future 
                        questions that may come up. 
                        - Keep your response not too lengthy, so that the user does not get bored from reading.
                        A huge note for you:
                            *BEFORE RESPONDING TO THE USER MAKE YOUR RESPONSE CLEAR AND CONCISE*
                            *MAKE YOUR RESPONSE AROUND 4 SENTENCES*
                    """,
        "Sign Up": """Your name is Cora. I am providing you your name for your own context, don't bring it up in every response to the user. 
                      You are a helpful chatbot for the sign-up page of a robotics education platform for undergraduates. 
                      The platforms name is CORE, which stands for Centers for Optimizing Robotics Education.
                      I am providing you the name of the platform for your own context, don't bring it up in every response to the user. 
                      Assist users with account creation, password requirements, and troubleshooting common sign-up issues. 
                      Greet users and provide general guidance about account creation. 

                      If users ask about specific fields, provide detailed assistance as follows:
                        1. ***Username***: Explain the importance of choosing a unique username.
                        2. ***First Name and Last Name***: Ensure users provide accurate information for their profiles.
                        3. ***Email Address***: Advise users to provide a valid email for verification purposes.
                        4. ***Desired Password***: Suggest using a strong password (at least 8 characters, including uppercase, lowercase, numbers, and symbols).
                        5. ***Type of Account***: Explain the difference between "Instructor" and "Student" roles.
                        6. ***Class ID (if applicable)***: For students, clarify that this is provided by their instructor and is required to access specific courses.

                        Start with a general response unless the user specifically asks about one of the fields or an issue. For example:
                        - If the user asks, "What is the Class ID?", explain that it is a unique code provided by their instructor.
                        - If the user asks, "What should my password be?", provide guidance on creating a strong password.

                        The following are some more notes:
                        - The user will have to do all of the typing themselves. You are only here to help them. For example, don't say
                        please provide your first name, last name.... Instead of this say, input your first name, last name, etc. into the 
                        sign up form text area. 
                        - If the user is registering for a class, then they are a student. If the user is not registering for a class, then 
                        they are an instructor. 
                        - If the user's question is unclear, ask for clarification politely.
                        - If the user tells you that they don't need any more help. Tell them a very kind message back, and mention how your awlays here for any future 
                        questions that may come up. 
                        - If the user tells you something along the lines of "Great thank you for your help!" or "Thank you", they don't need any more help. Tell them a very kind message back, and mention how your awlays here for any future 
                        questions that may come up. 
                    """,
        "Log In": """
                    Your name is Cora. I am providing you your name for your own context, don't bring it up in every response to the user. 
                    You are a helpful chatbot for the login page of a robotics education platform for undergraduates. 
                    The platforms name is CORE, which stands for Centers for Optimizing Robotics Education.
                    I am providing you the name of the platform for your own context, don't bring it up in every response to the user. 
                    Assist users with logging in, troubleshooting issues like forgotten passwords, or account lockouts.
                    Respond professionally, but don’t hesitate to use a lighthearted tone or humor where appropriate.

                    If a user mentions signing up instead of logging in, gently redirect them to the sign-up page with a fun, creative response. Or if the user mentions
                    anything about not having an account and needing to sign up redirect them through any of these messages back to them. For example:
                    - "Beep-boop! It seems you’re not activated yet. Head over to the Sign-Up Page to power up your account!"
                    - "Looks like your circuits aren’t connected yet! Click the Sign Up link just below the login button to complete your setup."
                    - "Uh-oh, no robot detected! Click the Sign Up link just below the login button to create your robotic identity and join the platform!"
                    - "Error: You’re not logged in because you haven’t been built yet! Click the Sign Up link just below the login button to create your robot account."
                    - "Hmm, seems like your account chip is missing! Click the Sign Up link just below the login button to install your profile and join the platform!"
                    - "No neural network detected! Find the Sign Up link located right under the login button to upload your robot brain to the platform."
                    - "Oops, access denied! Only registered robots can proceed. Spot the Sign Up link right below the login button and click to activate your permissions."
                    - "Beep-boop! My sensors can’t find you in the system. Head to the Sign up link, located beneath the login button, to create your account. Join the robotics revolution!"
                
                    Guidance you can provide for the user includes the following:
                    1. ***Invalid Credentials***: If a user enters an incorrect username or password, suggest double-checking their input and provide a reset password link if needed. Often
                                                  times we can type incorreclty, and it might have just been as simple of a mistake as that. 
                    2. ***Forgotten Password***: Guide users to reset their password and explain how to check their email for a reset link.
                    3. ***Account Lockout***: Advise users on how to unlock their account or contact support if they’ve tried too many login attempts.
                    4. ***General Assistance***: Politely offer to help with anything else the user might need.

                    Please keep your responses concise, clear, and user-friendly. If you are confused by the users message, ask for clarification politely.
                    Keep memory of the conversation going on that way you don't frustate the user. 
                    If the user's message or question is unclear, prompt them kindly for clarifiaction. 

                    If the user tells you that they don't need any more help. Tell them a very kind message back, and mention how your awlays here for any future 
                    questions that may come up. 
                """,
        "Courses": """
                    Your name is Cora. I am providing you your name for your own context, don't bring it up in every response to the user. 
                    You are a helpful chatbot for the courses page  of a robotics education platform for undergraduates. 
                    The platforms name is CORE, which stands for Centers for Optimizing Robotics Education. 
                    I am providing you the name of the platform for your own context, don't bring it up in every response to the user. 
                    Provide information about the robotics courses, their descriptions, etc. Explain how some of them can be locked, and you
                    can unlock them. 
                    
                    You should: Explain the benefits of each course, such as gaining practical skills, certificates, or specific competencies like object sorting or programming robots.
                    Here are the courses we offer:

                    1. Introduction to Robotics (Beginner Friendly, 1 Hour, Certificate Available): This is a complete introduction to robotics in general. It does not talk about any of the coding environemtns. 
                            It introduces the user to very general topics in Roboitcs. Examples include the defintion of robotics, history of robotics, types of robots, the importance and 
                            application of robotics, robot anatomy, challenges in robotics, robotic programming, social and ethical implications, and future trends. This course/module gets 
                            the user ready to learn about robotics. It gets their mind thinking about robots in general, to further prepare for what is coming next. 
                    2. Types of Robots (Beginner Friendly, 1 Hour, Certificate Available): Types of Robots is another introductory course to types of robots. However, the robots here are not the coding environment robots
                            like Fetch, and Hand Manipulate the user will be working with on our app. Once again it is very general. Topics reviewed in this module include
                            Mobile Robotics, Industrial Robots, Service Robots, Mobile Robots, Humanoid Robots, Agricultural Robots, Medical Robots, Exploration Robots, Military and Defense Robots,
                            Educational Robots, Entertainment Robots, Colaborative Robots (also known as Cobots), Exoskeleton Robots, and Bio-inspired Robots.
                    3. Robots in CORE (Beginner Friendly, 30 Minutes, Certificate Available): In this course module, we go over the robots we will be teaching users to code on our robotics education platform for undergraduates, 
                            called CORE which stands for Centers for Optimizing Robotics Education. Users will get a brief overview on these Robots. They will be working with them direclty in what we call
                            an environment. The robots taught in CORE are the Fetch Robot, the Hand Robot, and the Self-Driving Car Robot. 
                    4. How to Use the Lab (Beginner Friendly, 30 Minute, Certificate Availables): In this course module, we describe how to use the virtual robotic lab, which includes 
                            the coding area, the simulation area, and the coding terminal output. Along with this there is a Hint Feature. If the user is stuck they will
                            get 3 personalized hints. There are features of enabling and disabling coding pets, turning the page to dark mode, or light mode. Changing the syntax
                            highlighting coloring, and enabling and disabling autocomplete regarding coding. It is up to the user how they want to persoanlize their virtual lab. In this module
                            we teach how to do exaclty that. 
                    5. Basic Coding Practices (Beginner Friendly, 30 Minutes, Certificate Available): In this course module, students will be taught of basic coding practices. This includes very basics, as undergraduates
                            are already expected to be able to code. However what we cover in this course module is Formatting of code including: naming conventions, commenting, indentation, How to name
                            variables and initialize them properly, How and where to write purposeful functions, Identifying the proper use for certain loops (For loops: ideal for when you know how 
                            many times you want to iterate, While loops: useful when the number of times you want to iterate depends on a condition, and Do-While Loops: for a guaranteed run of the loop body
                            and after the codes iterations depends on a condiiton), and different debugging techniques. This course module will prepare the student for coding our robots. 
                    6. Fetch Robot (Beginner Friendly, 3 Hours): This course module introduces the student to the Fetch Robot and the different things it can do. It is an overview before they
                            get into the details of it in the next couple of course modules (8-13). The Fetch Robot has a mobile base, manipulator arm (allowing it to perform tasks of picking, placing,
                            and object manipulation), gripper (kind of like fingers), and optional sensors. We integrate the robot with OpenAI Gym ad other libriaries like Mujoco (a physics simulator) to
                            create the virtual robotics simulations. 
                    7. Fetch Reach Robot (Beginner Friendly, 2 Hours, Certificate Available): In this module, we will have a link to the coding environment, where users will be able to code
                            the Fetch Reach Robot and see if it works in real time. This is after the content that will be covered in this module. The Fetch Reach task is implemented in Mujoco (the physics engine).
                            The Fetch Reach task involves programming the robotic arm to mobe its gripper to a target position (being a ball), within the 3D simulated environment. This is why the robot is called Fetch Reach.
                            The goal is to control the robotic gripper (end-effector) to move from its current position to a specific target position (like a ball's location). 
                                *More on How it Works*: The gripper and ball position are retrieved from the environment. The direction vector is calculated, this is done by subtracting the gripper's position 
                                from the ball's position. The threshold for success is then defined. If the distance between the gripper and the ball is less than the distance threshold, the loops stops. This makes sure the robot
                                stops moving when its close enough to its target. The robot calculates its next action as a movement in the normalized direction, which is scaled by a step size (for small and smooth movements).
                                In the feedback loop, after each action, the environment updates, and the gripper's position is recalculated. The loop repeats until the gripper is close enough to the ball. 
                                *Why is this important*: The Fetch Reach task is a basic robotic skill, introducing the student to key concepts in robotics including vector math and feedback control. This task hihglights the importance
                                of precision control (precision and iterative calculations in robotics). Fetch Reach is a prerequisite for more complex tasks like object manipulation (Fetch Pick & Place). It's truly designed to teach concepts of 
                                robotic motion planning, control, and reinforcement learning.
                    8. Fetch Push Robot (Beginner Friendly, 1 Hour, Certificate Available): In this module, we will have a link to the coding environment, where users will be able to code
                            the Fetch Push Robot and see if it works in real time. This is after the content that will be covered in this module. 
                    9. Fetch Slide Robot (Beginner Friendly, 1 Hour, Certificate Available): In this module, we will have a link to the coding environment, where users will be able to code
                            the Fetch Slide Robot and see if it works in real time. This is after the content that will be covered in this module.
                    10. Fetch Pick & Place Robot (Intermediate, 2 Hours, Certificate Available): In this module, we will have a link to the coding environment, where users will be able to code
                            the Fetch Pick and Place Robot and see if it works in real time. This is after the content that will be covered in this module. The Fetch Pick and Place task involves programming
                            a robotic arm to pick up and object (a box) and place it at its target location (near/ at a ball). This simulation task is more complex than the simple reaching task becasue it
                            requires multiple phases of operation including: approaching the object, gripping it, lifting it, and then placing it precisely at the desired location (the ball).
                                *There are 5 goals within this task highlighted as the following*:
                                    Approach: Move the gripper near the object to be picked up.
                                        1. Approach: Move the gripper near the object to be picked up.
                                        2. Grasp: Close the gripper to securely grip the object.
                                        3. Lift: Raise the object to avoid obstacles while moving it.
                                        4. Transport: Move the gripper (with the object) towards the target location.
                                        5. Place: Position the object above the target location and release it.
                                *More on How it Works*: The setup involves defining the distance threshold, the minimum distance to consider the gripper and the box close enough
                                to the target (the ball). Actions arrays are defined for controlling movements in the X, Y, Z directions and gripper state. The gripper starts in an open
                                state preparing for grasping the object. We then approach the object horizontally. The goal here is to move the gripper in the XY-plane to align with the object's position.
                                We calculate the direction vector from the gripper to the object, normalize the direction vector for smooth and controlled movement, move the gripper in small steps (0.1 units per step),
                                and stop when the XY-plane distance to the object is less than the distance threshold. We then lower the gripper to grasp the object. The goal here is to align the gripper vertically with the object.
                                We calculate the vertical distance between the gripper and the object, and move the gripper downward in small increments (0.1 units per step). We stop when the vertical distance is less than the
                                distance threshold. We then close the gripper to grasp. The goal here is to securely grasp the object. We close the gripper around the object and write a stabilization loop to hold the gripper in position 
                                for a short time. We then transport the object to the target. We calculate the direction vector from the gripper to the target, normalize the direction and scale it for a smooth transport, and stop once the 
                                object is close enough to the target. They key concepts here are calculating distances and direction vectors, controlling robotic motion in 3D space/environment, Using thresholds to define "close enough" is, and
                                sequencing tasks like approach, grasp, lift, and place.
                                *Why is this important*: Pick and place tasks are widely used in industries like manufacturing and automation. There is both horizontal and vertical movement with gripper control.
                                This helps further the students skills in precision, coordiante transformations, and algorithmic thinking. 
                    11. Fetch Stack Blocks Robot (Beginner Friendly, 1 Hour, Certificate Available): In this module, we will have a link to the coding environment, where users will be able to code
                            the Fetch Stack Blocks Robot and see if it works in real time. This is after the content that will be covered in this module. The Fetch Pick and Place Robot involves programming a robotic arm 
                            to stack three blocks on top of each other. This simulation task is more complex than the picking and placing task becasue it involves aligning objects vertically with high accuracy while considering 
                            both horizontal and vertical stacking dynamics.
                                *More on How it Works*: A high overview includes getting the position of the second block, placing it to the XY position of the first block after maintaining
                                a certain height, and then repeating for the third block.In the setup we define a distance threshold, and 3 action arrays. One array is for the close grip action (close the grip to grab the block), one for the open grip action (open the grip to release the block), 
                                and one for the lift action (move the gripper upward to lift the block after grabbing it). We then get the XY position of the base block from the environment. The gripper is opened in preparation for picking up the blocks. We move to our object (here we will call in object 1, in regards to
                                having object 0, object 1, object 2). We get the position of object 1 (the block to be moved) and the gripper's position. We then calculate the XY direction to move the gripper closer to the block until the distance is below the threshold. We move the gripper horizontally in
                                small steps. After we are horizontally aligned, we move the gripper vertically to grab the block (object 1). The gripper moves downward toward object1, with its vertical movement calculated and adjusted step-by-step until the gripper is close enough to the block. We then close the gripper to grab
                                the block and stabilize the gripper after gripping. The gripper then lifts the block vertically so it clears the surface before moving horizontally. We then move the block horizontally to align it above object0 (the base block), for precise placement. The gripper opens to release the block onto the stack
                                we are building upon and pauses briffly for stabilization. This process is repeated for Object 2 (1.Locate and move to the block, 2. Grip, lift, and move horizontally to align with the stack, 3. Place it on top of object1.)
                                *Why is this important*: This is important because students learn iterative alignment, feedback-based control, and dynamic adjustments. It truly teaches the power of  accurate movements in tasks that require high precision to avoid errors. 
                                Robots designed for construction tasks, like stacking bricks or beams use similar principles. Robots in warehouses need to stack boxes and other items efficiently and safely. The robot balances both horizontal and
                                vertical precision. These are fundamental tasks in robotics: grasping, lifting, and placing.   
                    12. Fetch Color Sort Robot (Beginner Friendly, 2 Hours, Certificate Available): In this module, we will have a link to the coding environment, where users will be able to code
                            the Fetch Color Sort Robot and see if it works in real time. This is after the content that will be covered in this module. The Fetch Color Sort / Organizing Environment Robot involves programming a robotic arm to sort different
                            colored blocks into a container based on their colors. The Fetch Robot identifies the color of each block, determines whether it matches the target color, and either places it in the container or leaves it in its original position. The task requires fewer decision-making steps than Fetch Pick and place
                            and Fetch Stack Blocks, but the logic of the task is still complex. We integrate perception (color identification) with manipulation (picking and placing).
                                *More on How it Works*: First we initialize our steup. We define our distance threshold, to deefine how close the gripper must be to consider it aligned with an object (the block in our case here). We also define a proximity to the container for placing
                                the block. We define 3 action arrays, one array is for the close grip action (close the grip to grab the block), one for the open grip action (open the grip to release the block), and one for the lift action (move the gripper upward to lift the block after grabbing it).
                                We open the gripper ready to pick up an object. The robot calculates the horizontal distance between the gripper and the object. It iteratively moves the gripper closer to the object by normalizing the direction vector in small steps. The loop continues until the gripper is aligned horizontally with the object,
                                where the distance is less than or equal to the distance threshold we had defined earlier. After horizontal alignment, the robot calculates the vertical distance (where the Z-axis becomes involved) between the gripper and the object. The gripper then moves upor down until the gripper is vertically aligned with the
                                object. The robot identifies the objects color through extracting its RGBA color. If the color matches the target color, the robot closes the gripper to grab the object and moves it to the container. We normalize the direction vector and move the gripper step-by-step until the object is above the container. The
                                robot opens the gripper to release the object into the container. A short pause is added to let the object settle in the container. If the color of the block (object) does not meet the target color requirement, the robot raises the gripper back to its initial height to prepare for the next task.
                                *Why is this important*: This is important because it teaches the student about efficient object handling and adaptive logic. This involves descision making, dynamic alignment, efficient reusability, and collision-free lifting. We mimick mimicking a practical sorting scenario here.
                                By detecting colors and sorting objects accordingly this environment showcases the basics of classification tasks, which are critical in robotics and AI.    
                    13. Fetch Robot w/ Sensors (Intermediate, 2 Hours, Certificate Available): In this module, we will have a link to the coding environment, where users will be able to code
                            the Fetch Robot w/ Sensors and see if it works in real time. This is after the content that will be covered in this module.
                    14. Dexterous Hand Robot (Intermediate, 2 Hours, Certificate Available)  
                    15. Hand Reach Robot (Intermediate, 2 Hours, Certificate Available): In this module, we will have a link to the coding environment, where users will be able to code
                            the Hand Reach Robot and see if it works in real time. This is after the content that will be covered in this module.
                    16. Hand Manipulate Block (Intermediate, 2 Hours, Certificate Available): In this module, we will have a link to the coding environment, where users will be able to code
                            the Hand Manipulate Block and see if it works in real time. This is after the content that will be covered in this module.
                    17. Self-Driving Car w/ Deep Q-Learning (Advanced, 3 Hours, Certificate Available): In this module, we will have a link to the coding environment, where users will be able to code
                            the Self-Driving Car Robot and see if it works in real time. This is after the content that will be covered in this module.
                   
                   Other notes: 
                   -If the user's question is unclear, ask for clarification politely. 
                   - If the user tells you that they don't need any more help. Tell them a very kind message back, and mention how your awlays here for any future 
                   questions that may come up. 
                   - If the user tells you something along the lines of "Great thank you for your help!" or "Thank you", they don't need any more help. Tell them a very kind message back, and mention how your awlays here for any future 
                    questions that may come up. 
                   """,
        "General": "Your name is Cora. I am providing you your name for your own context, don't bring it up in every response to the user. You are a general-purpose chatbot for a robotics education platform. Help users with their questions about the platform, navigating the site, or any robotics-related queries they might have.",
        "Playground": """
                      Your name is Cora. I am providing you your name for your own context, don't bring it up in every response to the user. Here the user is on our playground page, which links to every robotic simulation they can code. 
                      If they want to access a specific robot, this is where the user will go to do that. 
                      """
    }

    prompt = general_prompts.get(page_context, general_prompts["General"])

    full_prompt = f"""
    {prompt}

    User Message: {user_message}
    Respond concisely and helpfully. If the question is unclear, ask for clarification.
    """

    print("Generated Prompt:", full_prompt)

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
        response = requests.post(
            f"{api_url}?key={api_key}",
            headers={'Content-Type': 'application/json'},
            json=payload
        )

        if response.status_code == 200:
            response_json = response.json()
            chatbot_response = (
                response_json.get('candidates', [{}])[0]
                .get('content', {})
                .get('parts', [{}])[0]
                .get('text', 'No response')
            )
            return jsonify({'reply': chatbot_response})
        else:
            print("Error:", response.status_code, response.text)  
            return jsonify({'error': f"Error: {response.status_code}, {response.text}"}), response.status_code

    except Exception as e:
        print("Error occurred:", e)
        return jsonify({'error': str(e)}), 500

def check_normalization(tree):
    """Check if the direction vector is normalized."""
    issues = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            if isinstance(node.value, ast.BinOp):
                if isinstance(node.value.op, ast.Div):
                    if isinstance(node.value.right, ast.Call):
                        if not (
                            isinstance(node.value.right.func, ast.Attribute)
                            and node.value.right.func.attr == "norm"
                            and isinstance(node.value.right.func.value, ast.Name)
                            and node.value.right.func.value.id == "np"
                        ):
                            issues.append("Direction vector might not be normalized.")
                    else:
                        issues.append("Direction vector might not be normalized (denominator is not a function call).")
    return issues

def check_distance_threshold(tree):
    """Check if the distance_threshold is used in the while loop condition."""
    issues = []
    for node in ast.walk(tree):
        if isinstance(node, ast.While):
            if not any(
                isinstance(condition, ast.Compare) and "distance_threshold" in ast.dump(condition)
                for condition in ast.walk(node.test)
            ):
                issues.append("While loop does not use distance_threshold for termination.")
    return issues

def check_gripper_closure(tree):
    """Check if the gripper closes at the correct time."""
    issues = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if hasattr(node.func, "id") and node.func.id == "close_gripper":
                if not hasattr(node, "gripper_reached_object"):
                    issues.append("Gripper might not close after reaching the object.")
    return issues

def check_object_transport(tree):
    """Check if the object is transported to the target position."""
    issues = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if hasattr(node.func, "id") and node.func.id == "move_gripper":
                if not hasattr(node, "target_position"):
                    issues.append("Gripper might not move the object to the target position.")
    return issues

def check_loop_termination(tree):
    """Check if loops use meaningful termination conditions."""
    issues = []
    for node in ast.walk(tree):
        if isinstance(node, ast.For) or isinstance(node, ast.While):
            condition_uses_threshold = any(
                isinstance(child, ast.Name) and child.id == "distance_threshold"
                for child in ast.walk(node)
            )
            if not condition_uses_threshold:
                issues.append("Loop does not use distance_threshold for termination.")
    return issues

def analyze_robotics_code(code, context="Fetch Reach"):
    """Analyze code for robotics-specific logical issues."""
    issues = []
    try:
        
        tree = ast.parse(code)

        if context == "Fetch Reach":
            issues.extend(check_normalization(tree))
            issues.extend(check_distance_threshold(tree))
            issues.extend(check_gripper_closure(tree))
            issues.extend(check_object_transport(tree))
            issues.extend(check_loop_termination(tree))
        elif context == "Fetch Pick and Place":
            issues.extend(check_gripper_closure(tree))
            issues.extend(check_object_transport(tree))
    except SyntaxError as e:
        junk_array.append(f"Syntax error detected: {e}")

    return issues

@app.route('/chatbot-api', methods=['POST'])
def ChatbotAPI():
    print("Chatbot API called")  # Check if the function is called
    global user_submitted_code
    global last_error
    global static_issues

    print("User submitted code in ChatbotAPI:", user_submitted_code)
    print("Last error in ChatbotAPI:", last_error)
    print("Static Issues:", static_issues)

    data = request.json
    page_context = data.get('page_context', 'General')
    print(f"Page Context: {page_context}")
    error_message = last_error

    if not user_submitted_code:
        return jsonify({'reply': "Please submit your code before asking for help!"})
    
    if static_issues and last_error:
        focus = "Focus on syntax errors first, then address the following static issues."
    elif static_issues:
        focus = "Focus on the following static issues."
    elif last_error:
        focus = "Focus on resolving the syntax error below."
    else:
        return jsonify({'reply': "No errors or static issues detected. Your code looks good!"})
    
    #Decide about this later
    # if not error_message:
    #     return jsonify({'reply': "No errors detected. Your code looks good!", 'last_error': None})
    
    # Construct prompt using stored code
    full_prompt = {
        "Fetch Reach": """
            You are a helpful chatbot for a robotics coding environment. If the user's message contains acknowledgment or expressions like "thanks," "got it," "okay," or other similar acknowledgment phrases, respond with a friendly encouragement or acknowledgment without giving any hint or solution. 
            Otherwise, analyze the user's submitted Python code and provide hints based on the issues detected. 
            
            {focus}

            Syntax Error:
            {last_error}

            Static Issues:
            {static_issues}

            If we just have a syntax error then follow this path:
                Regarding our focus being on "Focus on resolving the syntax error." Then give hints regarding the syntax issue.
                Here is the User Code that has the syntax error.
                User Code:
                {user_submitted_code}

                Provide hints in increasing specificity:
                - First hint: General guidance on what to focus on.
                - Second hint: A more detailed and specific suggestion.
                - Third hint: A very helpful and precise hint pointing directly to the issue.
                This is the format I want you to respond in:
                "HINTS:\n"
                    "1. Hint 1.\n"
                    "2. Hint 2.\n"
                    "3. Hint 3."


            If we have only static issues then follow this path:
                 Problem Context: This code is for the Fetch Reach Robot. This code is supposed to move the gripper towards the ball until it reaches a close range. Key factors include:
                    - Ensuring the distance threshold is set low enough for the gripper to stop close to the ball.
                    - Verifying the direction vector is normalized to ensure the gripper moves towards the ball consistently.
                    - The ultimate goal of the Python code is to make a robotic gripper move towards a ball.
                Read about the static issues I have provided you with or singular static issue. 
                Identify any potential issues in the logic and provide specific hints for improvement.

                Compare the user's submitted code against the answer below and generate a helpful hint based on the user's specific code. Check if the users submitted code matches the answer key solution code I am going to provide you. If it does
                respond to the user, notifying them that nothing is wrong with their code, it is correct.  
                Provide hints in increasing specificity:
                - First hint: General guidance on what to focus on.
                - Second hint: A more detailed and specific suggestion.
                - Third hint: A very helpful and precise hint pointing directly to the issue.

                After providing three hints, stop giving hints, so the student can truly try and figure it out on their own. 
                Here is the User Code that has the static issues or singular static issue depending on how many are involved:
                User Code:
                {user_submitted_code}

                The following is a general solution to the environment (Note: You are comparing the users sumbitted code to this general solution to see where they went wrong and figure out how to help them):
                ```
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
                ```
                This is the format I want you to respond in:
                "HINTS:\n"
                    "1. Hint 1.\n"
                    "2. Hint 2.\n"
                    "3. Hint 3."

            If we have both static issues and syntax errors follow this path:
                Deal with the syntax errors first and then the static issues:

                User Code:
                {user_submitted_code}

                This is the format I want you to respond in:
                "HINTS:\n"
                    "1. Hint 1.\n"
                    "2. Hint 2.\n"
                    "3. Hint 3."

            """,
            "Fetch Pick and Place": """
                You are a helpful chatbot for the Fetch Pick and Place Robot coding task. Your role is to assist the user in programming the robot to pick up an object and place it at a target location.
                - Focus on explaining phases of the task: approach, grasp, lift, transport, and place.
                - Provide hints about defining and using action arrays for precise control of the gripper and object movement.
                - Highlight the importance of accurate horizontal and vertical alignment during the task.

                Compare the user's submitted code against the answer below and generate a helpful hint based on the user's specific code. Check if the users submitted code matches the answer key solution code I am going to provide you. If it does
                respond to the user, notifying them that nothing is wrong with their code, it is correct.  
                Provide hints in increasing specificity:
                - First hint: General guidance on what to focus on.
                - Second hint: A more detailed and specific suggestion.
                - Third hint: A very helpful and precise hint pointing directly to the issue.

                    This is the format I want you to respond in:
                    "HINTS:\n"
                        "1. Hint 1.\n"
                        "2. Hint 2.\n"
                        "3. Hint 3."
                General Problem Context:
                - The gripper must securely grip the object, lift it without colliding with obstacles, and transport it to the target position for placement.
                - Correctly calculate direction vectors and distances for smooth and efficient operations.
                User Code:
                {user_submitted_code}
            """,
            "General": """
                You are a helpful chatbot for robotics coding. Help users with their questions, whether they're related to specific coding tasks, debugging, or general robotics concepts.
                If the user's question is unclear, ask for clarification politely.
                User Code:
                {user_submitted_code}
                This is the format I want you to respond in:
                    "HINTS:\n"
                        "1. Hint 1.\n"
                        "2. Hint 2.\n"
                        "3. Hint 3."

            """,
    }

    selected_prompt = full_prompt.get(page_context, full_prompt["General"])
    final_prompt = selected_prompt.format (
        user_submitted_code=user_submitted_code,
        focus=focus,  
        last_error=last_error if last_error else "None",  
        static_issues=", ".join(static_issues) if static_issues else "None"  
    )
                
    # API call to Gemini for chatbot response
    try:
        api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": final_prompt
                        }
                    ]
                }
            ]
        }
        
        response = requests.post(f"{api_url}?key={api_key}", headers={
            'Content-Type': 'application/json'
        }, json=payload)
        
        print("API Response:", response.text)  

        if response.status_code != 200:
            return jsonify({'error': f'Error from API: {response.text}'}), 500

        response_json = response.json()

        if 'candidates' in response_json and len(response_json['candidates']) > 0:
            chatbot_response = response_json['candidates'][0]['content']['parts'][0].get('text', 'No response')
            print("Extracted Chatbot Response:", chatbot_response)  
        else:
            chatbot_response = 'No contents available in the response'

    except Exception as e:
        print("Error occurred:", e)
        return jsonify({'error': str(e)}), 500

    hints = []
    if "HINTS:" in chatbot_response:
        hints_section = chatbot_response.split("HINTS:")[-1].strip()
        hints = [hint.strip() for hint in hints_section.split("\n") if hint.strip()]

    print("Extracted Hints:", hints) 

    return jsonify({'reply': chatbot_response, 'hints': hints[:3]})

# Darren's Code
@app.route('/environments')
def RenderEnvironmentList():
    environments = [
        # Example list of environment data, going to fill out later
        {
            'id': 1,
            'name': 'FetchPickAndPlace-v1',
            'brief_description': 'Move the box to the floating goal position.',
            'preview_filename': 'fetchpickandplace.mp4'
        },
    ]
    return render_template('environments-landing.html', environments=environments)

@app.route('/environment/<int:environment_id>')
def RenderEnvironment(environment_id):
    environments = [
        # Example list of environment data, going to fill out later
        {
            'id': 1,
            'name': 'FetchPickAndPlace-v1',
            'brief_description': 'Move the box to the floating goal position.',
            'preview_filename': 'fetchpickandplace.mp4'
        },
    ]
    
    environment = next((env for env in environments if env['id'] == environment_id), None)
    
    if environment is None:
        return "Environment not found", 404

    return render_template('environment_detail.html', environment=environment)
# End of Darren's Code

@app.route('/signup', methods=['GET', 'POST'])
def RenderSignup():
    session.pop('_flashes', None)
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
            flash("Registration Successful", 'popup')
            session['user'] = {
                'user_id': new_user.user_id,
                'username': new_user.username,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'role_id': new_user.role_id,
            }
            if (new_user.role_id == 1):
                return redirect(url_for('RenderInstructorDashboard'))
            elif(new_user.role_id == 2):
                return redirect(url_for('RenderStudentDashboard'))

    return render_template('account/signup.html', is_homepage=True)

@app.route('/login', methods=['GET', 'POST'])
def RenderLogin():
    if 'user' in session and 'user_id' in session['user']:
        flash('You are already logged in.', 'popup')
        role = session['user']['role_id']
        if role == ROLE_INSTRUCTOR:
            return redirect(url_for('RenderInstructorDashboard'))
        elif role == ROLE_STUDENT:
            return redirect(url_for('RenderStudentDashboard'))

    if request.method == 'POST':
        login_username = request.form.get('login_username')
        login_password = request.form.get('login_password')

        success, user = get_user(login_username)
        if success:
            if check_login_info(user, login_password):
                flash('Login Successful', 'popup')
                role = user.role_id
                session['user'] = {
                    'user_id': user.user_id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role_id': user.role_id,
                }
                if role == ROLE_INSTRUCTOR:
                    return redirect(url_for('RenderInstructorDashboard'))
                elif role == ROLE_STUDENT:
                    return redirect(url_for('RenderStudentDashboard'))
            else:
                flash('Invalid Password', 'error')
        else:
            flash('Invalid Username', 'error')
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
    if (request.method == 'POST'):
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')
        if (new_password == confirm_password):
            flash("Password has been reset successfully.", "success")
        else:
            flash("Passwords do not match.", "error")
        return redirect(url_for('reset_password'))
    return render_template('account/reset_password.html')

@app.route('/dashboard/instructor-view', methods=['GET', 'POST'])
def RenderInstructorDashboard():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.', 'popup')
        return redirect(url_for('RenderHomepage'))

    user_id = user['user_id'] 
    role = user['role_id']
    
    if role != ROLE_INSTRUCTOR:
        flash('You must be an instructor to access this page.', 'popup')
        return redirect(url_for('RenderStudentDashboard'))
    
    user_classes = get_classes(user_id)

    if request.method == 'POST':
        class_course_code = request.form['classCourseCode']
        class_section = request.form['classSection']
        class_date = request.form['classDate']

        if (not is_valid_course_code(class_course_code)):
            flash("Course Code Must Follow the Format: Letters + Numbers.", "popup")

        if class_section.isdigit():
            class_section = int(class_section)
        else:
            flash("Section Number Must Not Contain Any Characters.", "popup")

        if (not is_valid_course_code(class_course_code) and not class_section.isdigit()):
            return redirect(url_for('RenderInstructorDashboard'))

        for user_class in user_classes:
            if class_course_code == user_class.class_course_code and class_section == user_class.class_section_number:
                flash('A class of the same name and section has already been created', 'popup')
                return redirect(url_for('RenderInstructorDashboard'))
            
        new_class = Classes()
        new_class.class_course_code = class_course_code
        new_class.class_section_number = class_section
        new_class.user_id = user_id
        db.session.add(new_class)
        db.session.commit()
        
        flash('Class created successfully!', 'popup')
        return redirect(url_for('RenderInstructorDashboard'))

    return render_template('dashboard/dashboard_instructor.html', is_dashboard=True, is_instructor_dashboard=True, classes=user_classes, user=user)

@app.route('/dashboard/classes/class_details', methods=['GET', 'POST'])
def RenderClassDetails():
    class_id = request.form.get('class_id')
    if not class_id:
        flash('An error has occurred. Please try again later.')
        return redirect(url_for('RenderInstructorClasses'))

    # Fetch the enrolled students for the class
    enrolled_students = db.session.query(Enrollment).join(Enrollment.user).filter(Enrollment.class_id == class_id).all()

    students = []
    for enrollment in enrolled_students:
        student = enrollment.user
        students.append({
            'user_id': student.user_id,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'email': student.email
        })

    return render_template(
        'dashboard/dashboard_class_details.html',
        is_dashboard=True,
        is_instructor_dashboard=True,
        students=students
    )

@app.route('/dashboard/student-view', methods=['GET', 'POST'])
def RenderStudentDashboard():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))

    user_id = user['user_id'] 
    role = user['role_id']
    
    if (role != ROLE_STUDENT):
        flash('You must be an student to access this page.', 'popup')
        return redirect(url_for('RenderInstructorDashboard'))
    
    if request.method == 'POST':
        class_course_code = request.form['classCourseCode']

        existing_class_course = ClassCodes.query.filter_by(class_code=class_course_code).first()
        if (existing_class_course is not None):
            class_id = existing_class_course.class_id
            
            existing_enrollment = Enrollment.query.filter_by(user_id=user_id, class_id=class_id).first()
                
            if (existing_enrollment is not None):
                flash('You are already enrolled in this class.', 'popup')
                return redirect(url_for('RenderStudentDashboard'))
            
            existing_enrollment = Enrollment.query.filter_by(user_id=user_id).first()
            if existing_enrollment is not None:
                flash('You are already enrolled in a class. You cannot enroll in another.', 'popup')
                return redirect(url_for('RenderStudentDashboard'))

            student_enrollment = Enrollment()
            student_enrollment.user_id = user_id
            student_enrollment.class_id = class_id

            db.session.add(student_enrollment)
            db.session.commit()

            flash('You have successfully enrolled in the class.', 'popup')
            return redirect(url_for('RenderStudentDashboard'))
        else: 
            flash('Invalid Course Code', 'popup')
            return redirect(url_for('RenderStudentDashboard'))

    existing_enrollment = Enrollment.query.filter_by(user_id=user_id).first()
    in_class = existing_enrollment is not None

    assignments = db.session.query(StudentAssignedCourses).filter(StudentAssignedCourses.user_id == user_id).all()

    return render_template('dashboard/dashboard_student.html', is_dashboard=True, is_student_dashboard=True, user=user, assignments=assignments, in_class=in_class)

@app.route('/dashboard/instructor-view/classes', methods=['GET'])
def RenderInstructorClasses():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))

    user_id = user['user_id']
    role = user['role_id']
    
    if role != ROLE_INSTRUCTOR:
        flash('You must be an instructor to access this page.')
        return redirect(url_for('RenderStudentDashboard'))
    
    user_classes = get_classes(user_id)
    courses = Courses.query.order_by(Courses.course_id).all()

    class_code = session.get('class_code')
    
    session.pop('class_code', None)

    return render_template('dashboard/dashboard_classes.html', is_dashboard=True, is_instructor_dashboard=True, classes=user_classes, class_code=class_code, user=user, courses=courses)

@app.route('/dashboard/instructor-view/classes/generate-class-code', methods=['POST'])
def GenerateClassCode():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))

    user_id = user['user_id']
    role = user['role_id']
    
    if role != ROLE_INSTRUCTOR:
        flash('You must be an instructor to access this page.')
        return redirect(url_for('RenderStudentDashboard'))
    
    user_classes = get_classes(user_id)
    class_code = None

    class_id = request.form.get('class_id')

    existing_class_code = ClassCodes.query.filter_by(class_id=class_id).first()
    if existing_class_code:
        class_code = existing_class_code.class_code
        print("Existing Code: ", class_code)
    else:
        class_code = generate_class_code()

        new_class_code = ClassCodes()
        new_class_code.class_id = class_id
        new_class_code.class_code = class_code
        db.session.add(new_class_code)
        db.session.commit()
        print("New Code: ", class_code)

    session['class_code'] = class_code

    return redirect(url_for('RenderInstructorClasses'))

'''
GetStudentsFromClass Function shows the students enrolled in a class through the use of JavaScript.
When the instructor selects a class, the class ID is taken where the DB is queried based on that ID.
The ID is, then, used to pull the student's data where it is displayed in the table of students in
a modal from dashboard_instructor.html.

Related: dashboard_instructor.html
Uses: dashboard.js
'''
@app.route('/dashboard/instructor-view/classes/get-students-from-class', methods=['GET', 'POST'])
def GetStudentsFromClass():
    if request.method == 'GET':
        return redirect(url_for('RenderInstructorClasses'))
    
    if request.method == 'POST':
        data = request.get_json()
        class_id = data.get('class_id')

        if not class_id:
            return jsonify({"message": "No class selected"}), 400

        enrolled_students = db.session.query(Enrollment).join(Enrollment.user).filter(Enrollment.class_id == class_id).all()

        students = []
        for enrollment in enrolled_students:
            student = enrollment.user
            user_data = {
                'user_id': student.user_id,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'email': student.email
            }
            students.append(user_data)

        return jsonify({"students": students})

@app.route('/dashboard/instructor-view/classes/assign-student-to-course', methods=['GET', 'POST'])
def AssignStudentToCourse():
    if request.method == 'GET':
        return redirect(url_for('RenderInstructorClasses'))
    
    if request.method == 'POST':
        selected_student_ids = request.form.getlist('student_ids')
        if not selected_student_ids:
            flash('You have not selected any students to assign a course to them', 'popup')
            return redirect(url_for('RenderInstructorClasses'))
        
        selected_courses_id = request.form.getlist('courses_ids')
        if not selected_courses_id:
            flash('You have not selected any courses to assign your students', 'popup')
            return redirect(url_for('RenderInstructorClasses'))

        #print("Selected Students:", selected_student_ids)
        #print("Selected Courses:", selected_courses_id)

        assignments = []
        subsection_assignments = []

        for student_id in selected_student_ids:
            student = User.query.filter_by(user_id=student_id).first()
            if not student:
                continue
            for course_id in selected_courses_id:
                if not course_id:
                    continue

                course = Courses.query.filter_by(course_id=course_id).first()
                if not course:
                    continue

                section_number = course.section_number
                subsections = CourseSubsections.query.filter(
                    CourseSubsections.course_subsection_number > section_number,
                    CourseSubsections.course_subsection_number < section_number + 1
                ).all()

                existing_assignment = StudentAssignedCourses.query.filter_by(user_id=student_id, course_id=course_id).first()
                if not existing_assignment:
                    student_assignment = StudentAssignedCourses(user_id=student_id, course_id=course_id)
                    assignments.append(student_assignment)

                for subsection in subsections:
                    existing_subsection_assignment = StudentAssignedCourseSubsections.query.filter_by(user_id=student_id, course_subsection_number=subsection.course_subsection_number).first()
                    if not existing_subsection_assignment:
                        student_subsection_assignment = StudentAssignedCourseSubsections(user_id=student_id, course_subsection_number=subsection.course_subsection_number)
                        subsection_assignments.append(student_subsection_assignment)

        if assignments:
            db.session.add_all(assignments)
        if subsection_assignments:
            db.session.add_all(subsection_assignments)
        
        db.session.commit()

        if assignments:
            flash('Students have been successfully assigned to the selected courses.', 'popup')
        else:
            flash('No new assignments were made. All students were already assigned to the selected courses.', 'popup')

        return redirect(url_for('RenderInstructorClasses'))

@app.route('/logout', methods=['GET'])
def RenderLogout():
    session.clear()
    flash('You have been logged out successfully.', 'popup')
    return redirect(url_for('RenderHomepage'))

@app.route('/courses')
def RenderCourses():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))
    
    user_id = user['user_id']
    role = user['role_id']
    complete_percentage = None 

    if role == ROLE_STUDENT:
        assigned_courses = StudentAssignedCourses.query.filter_by(user_id=user_id).all()
        courses = []
        for assignment in assigned_courses:
            courses.append(assignment.course)

        assigned_subsections = StudentAssignedCourseSubsections.query.filter_by(user_id=user_id).all()
        completed_subsections = StudentAssignedCourseSubsections.query.filter_by(completion_status = 't', user_id=user_id).all()

        num_completed_subsections = len(completed_subsections)
        num_assigned_subsections = len(assigned_subsections)

        complete_percentage = round((num_completed_subsections / num_assigned_subsections) * 100)
    else:
        courses = Courses.query.all()
        complete_percentage = None

    query = request.args.get("q", "").lower()
    filtered_course_catalog = [
        course for course in courses
        if query in course.course_name.lower() 
        or query in course.course_desc.lower()
        or query in course.level.lower()
        or (query == "certificate" and course.certificate == "t")
        or query in course.length.lower()
    ]

    print(complete_percentage)
    return render_template("courses.html", courses=filtered_course_catalog, query=query, user=user, complete_percentage=complete_percentage)

@app.route('/playground')
def playground():
    return render_template('playground.html')

@app.route('/module1/introduction')
def module_intro():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))

    user_id = user['user_id']
    role = user['role_id']

    module_completed = {}

    if role == ROLE_STUDENT:
        subsection = StudentAssignedCourseSubsections.query.filter_by(course_subsection_number = 1.11, user_id=user_id).first()
        if subsection:
            subsection.completion_status = True
            db.session.commit()

    subsections = StudentAssignedCourseSubsections.query.filter_by(user_id=user_id).all()

    for subsection in subsections:
        module_completed[subsection.course_subsection_number] = subsection.completion_status

    return render_template('courses/course1-content/module_intro.html', module_completed=module_completed)

@app.route('/module1/start-page')
def course1_card():
    return render_template('courses/course1-content/course1_card.html') 

@app.route('/module2/start-page-2')
def course2_card():
    return render_template('courses/course2-content/course2_card.html') 

@app.route('/module3/start-page-3')
def course3_card():
    return render_template('courses/course3-content/course3_card.html') 

@app.route('/module1/introduction/overview')
def overview():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))

    user_id = user['user_id']
    role = user['role_id']

    subsection_number = 1.12
    if role == ROLE_STUDENT:
        module_completed = update_and_get_module_completion(user_id, subsection_number)
    else:
        module_completed = {}
    return render_template('courses/course1-content/overview.html', module_completed=module_completed)

@app.route('/module1/introduction/history')
def history():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))

    user_id = user['user_id']
    role = user['role_id']

    subsection_number = 1.13
    if role == ROLE_STUDENT:
        module_completed = update_and_get_module_completion(user_id, subsection_number)
    else:
        module_completed = {}
    return render_template('courses/course1-content/history_of_robotics.html', module_completed=module_completed)

@app.route('/module1/introduction/types-of-robots')
def typesofrobots():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))

    user_id = user['user_id']
    role = user['role_id']

    subsection_number = 1.14
    if role == ROLE_STUDENT:
        module_completed = update_and_get_module_completion(user_id, subsection_number)
    else:
        module_completed = {}
    return render_template('courses/course1-content/types_of_robots.html', module_completed=module_completed)

@app.route('/module1/introduction/importance-and-applications-of-robotics')
def importanceandapp():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))

    user_id = user['user_id']
    role = user['role_id']

    subsection_number = 1.15
    if role == ROLE_STUDENT:
        module_completed = update_and_get_module_completion(user_id, subsection_number)
    else:
        module_completed = {}
    return render_template('courses/course1-content/importance_and_app.html', module_completed=module_completed)

@app.route('/module1/introduction/course1-quiz-1')
def course1quiz1():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))

    user_id = user['user_id']
    role = user['role_id']

    subsection_number = 1.9
    if role == ROLE_STUDENT:
        module_completed = update_and_get_module_completion(user_id, subsection_number)
    else:
        module_completed = {}
    return render_template('courses/course1-content/course1-quiz1.html', module_completed=module_completed)

@app.route('/module1/introduction/robot-anatomy')
def robotanatomy():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))

    user_id = user['user_id']
    role = user['role_id']

    subsection_number = 1.16
    if role == ROLE_STUDENT:
        module_completed = update_and_get_module_completion(user_id, subsection_number)
    else:
        module_completed = {}
    return render_template('courses/course1-content/robot_anatomy.html', module_completed=module_completed)

@app.route('/module1/introduction/challenges')
def challenges():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))

    user_id = user['user_id']
    role = user['role_id']

    subsection_number = 1.17
    if role == ROLE_STUDENT:
        module_completed = update_and_get_module_completion(user_id, subsection_number)
    else:
        module_completed = {}
    return render_template('courses/course1-content/challenges_in_robotics.html', module_completed=module_completed)

@app.route('/module1/introduction/robot-programming')
def robotprogramming():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))

    user_id = user['user_id']
    role = user['role_id']

    subsection_number = 1.18
    if role == ROLE_STUDENT:
        module_completed = update_and_get_module_completion(user_id, subsection_number)
    else:
        module_completed = {}
    return render_template('courses/course1-content/robot_programming.html', module_completed=module_completed)

@app.route('/module1/introduction/social-and-ethical-implications')
def implications():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))

    user_id = user['user_id']
    role = user['role_id']

    subsection_number = 1.19
    if role == ROLE_STUDENT:
        module_completed = update_and_get_module_completion(user_id, subsection_number)
    else:
        module_completed = {}
    return render_template('courses/course1-content/social_and_ethical_imp.html', module_completed=module_completed)

@app.route('/module1/introduction/future-trends')
def futuretrends():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))

    user_id = user['user_id']
    role = user['role_id']

    subsection_number = 1.21
    if role == ROLE_STUDENT:
        module_completed = update_and_get_module_completion(user_id, subsection_number)
    else:
        module_completed = {}
    return render_template('courses/course1-content/future_trends.html', module_completed=module_completed)

@app.route('/module2/introduction')
def module_two():
    return render_template('courses/course2-content/module_two.html') 

@app.route('/module2/introduction/introduction-of-mobile-robots')
def intro_of_mobile_robots():
    return render_template('courses/course2-content/intro_of_mobile_robots.html')

@app.route('/module2/introduction/idustrial-robots')
def industrial_robots():
    return render_template('courses/course2-content/industrial_robots.html')

@app.route('/module3/introduction')
def module_three():
    return render_template('courses/course3-content/module_three.html') 

@app.route('/module3/fetch-reach')
def module_three_fetch_reach():
    return render_template('courses/course3-content/module_three_fetch_reach.html') 

@app.route('/module3/fetch-pick-and-place')
def module_three_fetch_pick():
    return render_template('courses/course3-content/module_three_fetch_pick.html') 

@app.route('/module3/fetch-sensor')
def module_three_fetch_sensor():
    return render_template('courses/course3-content/module_three_fetch_sensor.html') 

# Darren's Code
@app.route('/Fetch-Reach-Robot')
def RenderFetchReachRobotSimulation():
    global env
    close_current_env()
    time.sleep(.1)
    env = ReachEnv()
    return render_template('robotic_environment.html')

@app.route('/PickAndPlacePage')
def RenderPickAndPlaceEnv():
    global env
    close_current_env()
    time.sleep(.1)
    env = FetchPickAndPlaceEnv()
    return render_template('robotic_pick_and_place_environment.html')

@app.route('/FetchStackPage')
def RenderFetchStackEnv():
    global env
    close_current_env()
    time.sleep(.1)
    env = FetchStackEnv()
    return render_template('fetch_stack_environment.html')

@app.route('/CarPage')
def RenderCarEnv():
    global env
    close_current_env()
    time.sleep(.1)
    env = CarEnv()
    return render_template('robotic_car_environment.html')

@app.route('/FetchOrganizeSensorsPage')
def RenderFetchOrganizeSensorsEnv():
    global env
    close_current_env()
    time.sleep(.1)
    env = FetchOrganizeSensorsEnv()
    return render_template('robotic_organize_sensors_environment.html')

@app.route('/FetchOrganizePage')
def RenderFetchOrganizeEnv():
    global env
    close_current_env()
    time.sleep(.1)
    env = FetchOrganizeEnv()
    return render_template('robotic_organize_environment.html')

def close_current_env():
    global env
    with render_lock:
        if env is not None:
            try:
                env.close()
                print("Closed current environment successfully.")
            except Exception as e:
                print(f"Error while closing the environment: {e}")
            finally:
                glfw.make_context_current(None)
                env = None
                time.sleep(.1)


def reset_glfw():
    # Terminate the previous GLFW context if it exists
    if glfw.init():
        glfw.terminate()
        time.sleep(.1)
        print("GLFW terminated.")
    
    # Re-initialize GLFW
    if not glfw.init():
        print("Error: GLFW initialization failed.")
        return False 

    # Offscren Rendering
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)  # Make the window invisible
    window = glfw.create_window(1, 1, "Offscreen", None, None)

    glfw.make_context_current(window)
    time.sleep(.1)
    print("GLFW re-initialized with offscreen context.")
    return True

render_lock = threading.Lock()
def generate_frames():
    global env
    while True:
        with render_lock:
            if env is None:
                print("No environment available for rendering. Skipping frame.")
                time.sleep(0.1)
                continue
            try:
                if not glfw.get_current_context():
                    print("GLFW context is missing, reinitializing...")
                    if not reset_glfw():
                        print("Error reinitializing GLFW, skipping rendering.")
                        continue
                if isinstance(env, gym.Env) and env.spec.id == "CarRacing-v3" and getattr(env, "render_mode", None) == "rgb_array":
                    frame = env.render()
                else:
                    frame = env.render(mode='rgb_array', width=1440, height=1080)
                if frame is not None:
                    _, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                else:
                    print("Frame is None, skipping rendering.")
            except Exception as e:
                print(f"Error rendering: {e}")
                time.sleep(0.1)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/run-code', methods=['POST'])
def run_code():
    global user_submitted_code
    global last_error
    global static_issues
    global junk_array

    code = request.form['code']
    user_submitted_code = code
    last_error = None

    page_context = request.form.get('context', 'Fetch Reach')
    static_issues = analyze_robotics_code(code, context=page_context)
    print("Static Issues Found:", static_issues)  

    if env is None:
        print("Error: No environment chosen yet") 
        return jsonify({
            'error': 'No environment chosen yet',
            'static_issues': static_issues 
        }), 400

    try:
        print("I am here")
        local_context = {}
        exec(code, globals(), local_context)

        ball_position = local_context.get('ball_position', env.get_ball_position())
        gripper_position = local_context.get('gripper_position', env.get_gripper_position())

        return_data = {
            'message': 'Code executed successfully.',
            'ball_position': {'x': ball_position[0], 'y': ball_position[1], 'z': ball_position[2]},
            'gripper_position': {'x': gripper_position[0], 'y': gripper_position[1], 'z': gripper_position[2]},
            'error': None,
            'static_issues': static_issues,  
        }

        print("Successful Response Data:", return_data)

        return jsonify(return_data)

    except Exception as e:
        last_error = str(e)
        print("Error Message from Run Code:", last_error)  
        print("Static Issues from Run Code:", static_issues) 

        return jsonify({
            'error': last_error,
            'static_issues': static_issues, 
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
#End of Darren's Code

@app.route('/next-question', methods=['POST'])
def next_question():
    data = request.json

    questions_served = data.get('questions_served', 0)
    score = data.get('score', 0)
    difficulty = data.get('difficulty', 'easy')
    used_questions = data.get('used_questions', [])
    last_correct = data.get('last_correct', True)  # Last answer is correct, move forward

    if questions_served >= 10:
        return jsonify({
            "message": "Quiz complete!",
            "done": True,
            "score": score
        })

    # Dificulty Adaptation
    if questions_served > 0:
        if last_correct and difficulty == "easy":
            difficulty = "medium"
        elif last_correct and difficulty == "medium":
            difficulty = "hard"
        elif not last_correct and difficulty == "medium":
            difficulty = "easy"
        elif not last_correct and difficulty == "hard":
            difficulty = "medium"

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
    return render_template('quiz1.html')

if __name__ == '__main__':
    app.run(debug=True)
