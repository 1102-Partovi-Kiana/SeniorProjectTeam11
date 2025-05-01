from flask import Flask, render_template, request, jsonify, Response, flash, redirect, url_for, session, send_file, send_from_directory
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
from PIL import Image, ImageDraw, ImageFont
import io
from datetime import datetime, timedelta, time as datetime_time
import matplotlib.pyplot as plt
import base64
from sqlalchemy import func
import os
import traceback
import requests
from flask import send_file
from PIL import Image, ImageDraw, ImageFont
import io
from reportlab.pdfgen import canvas
from quiz.course1_quiz1 import quiz_data as quiz
import json
from quiz.course1_quiz1_2 import quiz_data as quiz
from quiz.course2_quiz2 import quiz_data as quiz
from quiz.course3_quiz3 import quiz_data as quiz
from quiz.course4_quiz4 import quiz_data as quiz
from quiz.course6_quiz6 import quiz_data as quiz
from quiz.course7_quiz7 import quiz_data as quiz
from quiz.course8_quiz8 import quiz_data as quiz
from quiz.course9_quiz9 import quiz_data as quiz
from quiz.course10_quiz10 import quiz_data as quiz
from quiz.course11_quiz11 import quiz_data as quiz
from urllib.parse import quote, unquote

app = Flask(__name__, static_folder='static')
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
mail.init_app(app)

app.config.update(
    SESSION_TYPE="redis",
    SESSION_REDIS="redis://localhost:6379/0",
    PERMANENT_SESSION_LIFETIME=timedelta(hours=1)
)


ROLE_INSTRUCTOR = 1
ROLE_STUDENT = 2
ROLE_ADMIN = 3
CERTIFICATE_TEMPLATE = "static/certificate_template.png"

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

@app.route('/Chatbot')
def RenderChatbot():
    return render_template('chatbot.html')

attempt_counter = 0
user_submitted_code = ""
last_error = None
static_issues = []
junk_array = []
api_key = "AIzaSyD9sgZ36638e7fsk5rK5j0uDNGl-zy6hUU " 
#AIzaSyAfoQ856qhys1OONDyPMRR7LoArpKz2JSY


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

import ast

# ---------------- Static Analysis Functions for FETCH REACH ROBOT -------------------------#
def check_object_transport_fetch_reach(tree):
    """Check that the object is transported properly with the call to `env.step()` in the environment."""
    issues = []
    any_step_call_found = False
    valid_step_call_found = False
    all_line_numbers = [node.lineno for node in ast.walk(tree) if hasattr(node, "lineno")]
    last_line_number = max(all_line_numbers) if all_line_numbers else "Unknown"
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if (isinstance(node.func, ast.Attribute) and
                isinstance(node.func.value, ast.Name) and 
                node.func.value.id == "env" and 
                node.func.attr == "step"):
                any_step_call_found = True
                if node.args and len(node.args) > 0:
                    valid_step_call_found = True
                else:
                    line_number = getattr(node, "lineno", last_line_number)
                    issues.append({
                        "message": "env.step() is called without an action argument.",
                        "line": line_number
                    })
    if not any_step_call_found:
        issues.append({
            "message": "No call to env.step() was found.",
            "line": last_line_number
        })
    elif not valid_step_call_found and not issues:
        issues.append({
            "message": "No call to env.step() with an action argument was found.",
            "line": last_line_number
        })
    return issues

def check_ball_position_retrieval_fetch_reach(tree):
    """Check that `env.get_ball_position()` is used to get the ball position."""
    issues = []
    last_line_number = 1
    ball_position_called = False

    for node in ast.walk(tree):
        if hasattr(node, "lineno"):
            last_line_number = node.lineno  

        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name) and node.func.value.id == "env":
                if node.func.attr == "get_ball_position":
                    ball_position_called = True

    if not ball_position_called:
        issues.append({
            "message": "Missing call to `env.get_ball_position()`. This function needs to be called somewhere in the code to retrieve the ball position from the environment.",
            "line": last_line_number
        })

    return issues

def check_gripper_position_retrieval_fetch_reach(tree):
    """Check that `env.get_gripper_position()` is called to get the gripper position."""
    issues = []
    last_line_number = 1
    gripper_position_called = False

    for node in ast.walk(tree):
        if hasattr(node, "lineno"):
            last_line_number = node.lineno  

        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if (isinstance(node.func.value, ast.Name) and node.func.value.id == "env"
                    and node.func.attr == "get_gripper_position"):
                gripper_position_called = True

    if not gripper_position_called:
        issues.append({
            "message": "Missing call to `env.get_gripper_position()`. This function needs to be called somewhere in the code to retrieve the gripper position from the environment.",
            "line": last_line_number
        })

    return issues

def variable_from_np_array(node):
    """If node is of the form np.array(variable), return the variable name. Otherwise, return None."""
    if (isinstance(node, ast.Call) and
        isinstance(node.func, ast.Attribute) and
        isinstance(node.func.value, ast.Name) and
        node.func.value.id == "np" and
        node.func.attr == "array" and
        node.args and isinstance(node.args[0], ast.Name)):
        return node.args[0].id
    return None

def check_direction_computation_fetch_reach(tree):
    """Check the direction vector is computed correctly, with the correct operation, correct subtraction order, correct variable names, and tracks the user's direction variable name."""

    issues = []
    last_line_number = 1
    direction_assigned = False
    incorrect_operation = None
    incorrect_order = False
    undefined_variable = False

    ball_var = None
    gripper_var = None
    user_left_var = None
    user_right_var = None
    direction_var = "direction"  

    for node in ast.walk(tree):
        if hasattr(node, "lineno"):
            last_line_number = node.lineno  
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            if (isinstance(node.value.func, ast.Attribute) and 
                isinstance(node.value.func.value, ast.Name) and 
                node.value.func.value.id == "env"):
                if node.value.func.attr == "get_ball_position":
                    if isinstance(node.targets[0], ast.Name):
                        ball_var = node.targets[0].id  
                elif node.value.func.attr == "get_gripper_position":
                    if isinstance(node.targets[0], ast.Name):
                        gripper_var = node.targets[0].id  

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.BinOp):
            if isinstance(node.targets[0], ast.Name):
                direction_assigned = True
                direction_var = node.targets[0].id 

                if not isinstance(node.value.op, ast.Sub):
                    incorrect_operation = node.value.op

                left_var = variable_from_np_array(node.value.left)
                right_var = variable_from_np_array(node.value.right)

                if left_var and right_var:
                    user_left_var = left_var
                    user_right_var = right_var

                    if user_left_var not in [ball_var, gripper_var] or user_right_var not in [ball_var, gripper_var]:
                        undefined_variable = True

                    if user_left_var == gripper_var and user_right_var == ball_var:
                        incorrect_order = True

    if not direction_assigned:
        issues.append({
            "message": f"Missing computation of direction. Make sure you define `{direction_var} = np.array({ball_var}) - np.array({gripper_var})`.",
            "line": last_line_number
        })

    if incorrect_operation:
        issues.append({
            "message": f"Incorrect operation used in direction computation. Expected subtraction (-), but found {type(incorrect_operation).__name__}.",
            "line": last_line_number
        })

    if incorrect_order:
        issues.append({
            "message": f"Incorrect subtraction order. Expected `{direction_var} = np.array({ball_var}) - np.array({gripper_var})`, but found `{direction_var} = np.array({user_left_var}) - np.array({user_right_var})`.",
            "line": last_line_number
        })

    if undefined_variable:
        issues.append({
            "message": f"Incorrect variable usage in {direction_var} computation. Both variables need to come from `env.get_ball_position()` and `env.get_gripper_position()`.",
            "line": last_line_number
        })

    return issues

def check_np_array_wrapping_fetch_reach(tree):
    """Check if ball_position and gripper_position are wrapped in np.array() before subtraction.
       If one of them or all of them are missing, exact messages will be told to the user.
    """
    issues = []
    last_line_number = 1
    ball_var = None
    gripper_var = None

    for node in ast.walk(tree):
        if hasattr(node, "lineno"):
            last_line_number = node.lineno  
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            if (isinstance(node.value.func, ast.Attribute) and 
                isinstance(node.value.func.value, ast.Name) and 
                node.value.func.value.id == "env"):
                if node.value.func.attr == "get_ball_position":
                    if isinstance(node.targets[0], ast.Name):
                        ball_var = node.targets[0].id  
                elif node.value.func.attr == "get_gripper_position":
                    if isinstance(node.targets[0], ast.Name):
                        gripper_var = node.targets[0].id  

    def is_np_array_call(expr):
        return (isinstance(expr, ast.Call) and
                isinstance(expr.func, ast.Attribute) and
                isinstance(expr.func.value, ast.Name) and
                expr.func.value.id == "np" and 
                expr.func.attr == "array")

    for node in ast.walk(tree):
        if (isinstance(node, ast.Assign) and isinstance(node.value, ast.BinOp) and 
            isinstance(node.value.op, ast.Sub)):
            left = node.value.left
            right = node.value.right

            if not is_np_array_call(left):
                issues.append({
                    "message": f"`{ball_var}` must be wrapped in `np.array()` before subtraction.",
                    "line": node.lineno
                })
            if not is_np_array_call(right):
                issues.append({
                    "message": f"`{gripper_var}` must be wrapped in `np.array()` before subtraction.",
                    "line": node.lineno
                })
    return issues

def check_direction_normalization_fetch_reach(tree):
    """Check that the direction vector is normalized correctly with the correct variable involved."""
    issues = []
    last_line_number = 1
    normalization_found = False
    incorrect_variable_used = False
    direction_var = None  

    for node in ast.walk(tree):
        if hasattr(node, "lineno"):
            last_line_number = node.lineno
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.BinOp):
            if isinstance(node.value.op, ast.Sub):
                if node.targets and isinstance(node.targets[0], ast.Name):
                    direction_var = node.targets[0].id

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            if (isinstance(node.value.func, ast.Attribute) and 
                isinstance(node.value.func.value, ast.Attribute) and 
                node.value.func.value.attr == "linalg"):
                normalization_found = True 
                if node.value.func.attr == "norm":
                    if node.value.args and isinstance(node.value.args[0], ast.Name):
                        if node.value.args[0].id != direction_var:
                            incorrect_variable_used = True
                    else:
                        incorrect_variable_used = True
                else:
                    incorrect_variable_used = True

    if not normalization_found:
        issues.append({
            "message": f"Missing computation of direction normalization. Expected np.linalg.norm({direction_var}).",
            "line": last_line_number
        })
    elif incorrect_variable_used:
        issues.append({
            "message": f"Incorrect variable used inside `np.linalg.norm()`. Expected {direction_var}, but found a different variable or incorrect normalization function.",
            "line": last_line_number
        })

    return issues

def check_for_loop_usage_fetch_reach(tree):
    """Check if a for loop is used. If so, add an issue because a while loop is required."""
    issues = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.For):
            issues.append({
                "message": "A for loop was used. Please use a while loop instead.",
                "line": node.lineno
            })
    
    return issues

def check_loop_termination_fetch_reach(tree):
    """Check if loops use meaningful termination conditions."""
    issues = []
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.For, ast.While)):
            condition_uses_threshold = any(
                (isinstance(child, ast.Name) and child.id == "distance_threshold") or
                (isinstance(child, ast.Constant) and isinstance(child.value, (int, float)) and child.value == 0.01)
                for child in ast.walk(node)
            )
            if not condition_uses_threshold:
                issues.append({
                    "message": "While Loop does not use distance_threshold or 0.01 for termination.",
                    "line": node.lineno  # AST nodes have this attribute
                })
    
    return issues

def check_while_loop_normalized_comparison_fetch_reach(tree):
    """Check that the while loop condition uses a normalized variable (computed via np.linalg.norm(...)) compared to distance_threshold."""
    issues = []
    
    normalized_vars = set()
    for node in ast.walk(tree):
        if hasattr(node, "lineno"):
            last_line_number = node.lineno
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            func = node.value.func
            if (isinstance(func, ast.Attribute) and 
                isinstance(func.value, ast.Attribute) and 
                isinstance(func.value.value, ast.Name) and 
                func.value.value.id == "np" and 
                func.value.attr == "linalg" and 
                func.attr == "norm"):
                if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                    normalized_vars.add(node.targets[0].id)

    for node in ast.walk(tree):
        if isinstance(node, ast.While):
            cond = node.test
            if isinstance(cond, ast.Compare):
                if not (len(cond.ops) == 1 and len(cond.comparators) == 1):
                    issues.append({
                        "message": "The while loop condition must have a single comparison.",
                        "line": node.lineno
                    })
                    continue

                if not isinstance(cond.ops[0], ast.Gt):
                    issues.append({
                        "message": "The while loop condition must use the '>' operator.",
                        "line": node.lineno
                    })

                if isinstance(cond.left, ast.Name):
                    normalized_var_used = cond.left.id
                    if normalized_var_used not in normalized_vars:
                        issues.append({
                            "message": f"The variable used in the while loop condition ('{normalized_var_used}') is not computed using np.linalg.norm(...).",
                            "line": node.lineno
                        })
                else:
                    issues.append({
                        "message": "The left-hand side of the while loop condition should be a variable computed by np.linalg.norm(...).",
                        "line": node.lineno
                    })

            else:
                issues.append({
                    "message": "The while loop condition must be a comparison (e.g., normalized_value > distance_threshold).",
                    "line": node.lineno
                })
    return issues


# ---------------- Static Analysis Functions for FETCH PICK AND PLACE ROBOT -------------------------#


# ---------------- Static Analysis Functions for FETCH ORGANIZE ROBOT -------------------------#
def check_undefined_variables_fetch_organize(tree):
    """Check for variables that are used but not defined in the code."""
    issues = []
    defined_vars = set()
    used_vars = set()
    last_line_number = 1  

    for node in ast.walk(tree):
        if hasattr(node, "lineno"):
            last_line_number = node.lineno  

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    defined_vars.add(target.id)

        elif isinstance(node, ast.FunctionDef):
            defined_vars.add(node.name)
            for arg in node.args.args:
                defined_vars.add(arg.arg)

        elif isinstance(node, ast.Name):
            used_vars.add(node.id)

    assumed_defined_vars = {"env", "float", "np", "print", "range", "abs", "_"}

    undefined_vars = used_vars - defined_vars - assumed_defined_vars

    for var in undefined_vars:
        issues.append({
            "message": f"Variable '{var}' is used but not defined.",
            "line": last_line_number  
        })

    return issues

def check_site_xpos_object_name_usage_twice_fetch_organize(tree):
    """Check that `env.sim.data.get_site_xpos(object_name)` is used exactly twice."""
    issues = []
    last_line_number = 1
    xpos_call_count = 0

    for node in ast.walk(tree):
        if hasattr(node, "lineno"):
            last_line_number = node.lineno  

        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if (
                node.func.attr == "get_site_xpos"
                and isinstance(node.func.value, ast.Attribute)
                and node.func.value.attr == "data"
                and len(node.args) > 0  
            ):
                arg = node.args[0]  

                if isinstance(arg, ast.Name):
                    xpos_call_count += 1

    if xpos_call_count < 2:
        issues.append({
            "message": f"`env.sim.data.get_site_xpos(object_name)` is used only {xpos_call_count} times. It must be used exactly twice within the code.",
            "line": last_line_number
        })
    elif xpos_call_count > 2:
        issues.append({
            "message": f"`env.sim.data.get_site_xpos(object_name)` is used {xpos_call_count} times. It must be used exactly twice within the code.",
            "line": last_line_number
        })

    return issues

def check_site_xpos_robot_grip_usage_three_times_fetch_organize(tree):
    """Check that `env.sim.data.get_site_xpos('robot0:grip')` is used exactly three times."""
    issues = []
    last_line_number = 1
    xpos_call_count = 0

    for node in ast.walk(tree):
        if hasattr(node, "lineno"):
            last_line_number = node.lineno  

        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if (
                node.func.attr == "get_site_xpos"
                and isinstance(node.func.value, ast.Attribute)
                and node.func.value.attr == "data"
                and len(node.args) > 0
            ):
                arg = node.args[0]

                if isinstance(arg, ast.Constant) and arg.value == "robot0:grip":
                    xpos_call_count += 1

    if xpos_call_count < 3:
        issues.append({
            "message": f"`env.sim.data.get_site_xpos('robot0:grip')` is used only {xpos_call_count} times. It must be used exactly twice.",
            "line": last_line_number
        })
    elif xpos_call_count > 3:
        issues.append({
            "message": f"`env.sim.data.get_site_xpos('robot0:grip')` is used {xpos_call_count} times. It must be used exactly twice.",
            "line": last_line_number
        })

    return issues

def check_opens_gripper_first_fetch_organize(tree):
    """Check the first env.step() call is applied to open_grip_action."""
    issues = []
    first_env_step_found = False

    for node in ast.walk(tree):
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            func = node.value.func
            if (
                isinstance(func, ast.Attribute) and
                func.attr == "step" and
                isinstance(func.value, ast.Name) and func.value.id == "env"
            ):
                first_env_step_found = True
                if (
                    len(node.value.args) > 0 and
                    isinstance(node.value.args[0], ast.Name) and
                    node.value.args[0].id == "open_grip_action"
                ):
                    return issues 
                
                else:
                    issues.append({
                        "message": "The first 'env.step()' call must use 'open_grip_action' to open the gripper.",
                        "line": node.lineno
                    })
                    return issues  

    if not first_env_step_found:
        issues.append({
            "message": "Missing 'env.step(open_grip_action)' at the beginning to open the gripper.",
            "line": 1
        })

    return issues

def check_env_step_usage_in_while_loops_fetch_organize(tree):
    """Checks if all `while True:` loops contain at least one call to `env.step()`."""
    issues = []
    last_line_number = 1

    for node in ast.walk(tree):
        if hasattr(node, "lineno"):
            last_line_number = node.lineno  

        if isinstance(node, ast.While): 
            contains_env_step = any(
                isinstance(child, ast.Expr) and
                isinstance(child.value, ast.Call) and
                isinstance(child.value.func, ast.Attribute) and
                child.value.func.attr == "step"
                for child in ast.walk(node)
            )
            if not contains_env_step:
                issues.append({
                    "message": "Missing `env.step()` inside a while loop, which may cause an infinite loop.",
                    "line": last_line_number
                })

    return issues

def check_closes_gripper_after_vertical_fetch_organize(tree):
    """Checks if the `env.step(close_grip_action)` after the vertical reach"""
    issues = []
    close_found = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if (isinstance(node.func, ast.Attribute) and 
                isinstance(node.func.value, ast.Name) and 
                node.func.value.id == "env" and 
                node.func.attr == "step"):
                for arg in node.args:
                    if isinstance(arg, ast.Name) and arg.id == "close_grip_action":
                        close_found = True
                        break
            if close_found:
                break
    if not close_found:
        issues.append({
            "message": "Missing env.step(close_grip_action) in the code.",
            "line": 1
        })
    return issues

def check_horizontal_distance_subtraction_fetch_organize(tree):
    """Check NumPy array subtraction is used for computing distances (e.g., horizontal_distance)."""
    issues = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):  
            if isinstance(node.value, ast.BinOp):  
                if isinstance(node.value.left, ast.Call) and isinstance(node.value.right, ast.Call):
                    if isinstance(node.value.left.func, ast.Attribute) and isinstance(node.value.right.func, ast.Attribute):
                        if node.value.left.func.attr == "array" and node.value.right.func.attr == "array":
                            if isinstance(node.value.op, (ast.Add, ast.Mult, ast.Div)): 
                                issues.append({
                                    "message": f"Distance calculation should use subtraction (-), but found {type(node.value.op).__name__}.",
                                    "line": node.lineno
                                })

    return issues

# ---------------- Static Analysis Functions for FETCH SENSORS ROBOT -------------------------#
def check_one_env_step_sensors(tree):
    """Check that at least one call to env.step() is present."""
    issues = []
    found = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if hasattr(node.func, 'attr') and node.func.attr == "step":
                found = True
                break
    if not found:
        issues.append({
            "message": "No call to env.step() found in the code.",
            "line": None
        })
    return issues

def check_loop_termination_sensors(tree):
    """
    Check for while loops that use a constant True test without a break.
    This is a heuristic to catch potential infinite loops.
    """
    issues = []
    for node in ast.walk(tree):
        if isinstance(node, ast.While):
            # Look for a "while True:" loop
            if (isinstance(node.test, ast.NameConstant) and node.test.value is True) or \
               (hasattr(node.test, 'value') and node.test.value is True):
                # Check if any break is present in the loop body
                has_break = any(isinstance(n, ast.Break) for n in ast.walk(node))
                if not has_break:
                    issues.append({
                        "message": "Infinite while loop detected without a break condition.",
                        "line": node.lineno
                    })
    return issues

def check_forward_sensor_value_assignment_sensors(tree):
    """Check that the forward sensor value is assigned from the correct `env.get_sensor_forward_value()` function."""
    issues = []
    expected_sensor_functions = { "get_sensor_forward_value" }

    found_sensors = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            if (isinstance(node.value.func, ast.Attribute) and 
                isinstance(node.value.func.value, ast.Name) and 
                node.value.func.value.id == "env"):

                func_name = node.value.func.attr
                if func_name in expected_sensor_functions:
                    found_sensors.add(func_name)

    missing_sensors = expected_sensor_functions - found_sensors
    for missing in missing_sensors:
        issues.append({
            "message": f"Missing or incorrect call to `env.{missing}()`. Check the required sensor value is retrieved.",
            "line": 1  
        })

    return issues

def check_while_loop_sensor_condition_sensors(tree):
    """Check whether a `while` loop correctly uses and updates a sensor variable assigned from `env.get_sensor_forward_value()`."""
    issues = []
    sensor_variable = None

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            if (isinstance(node.value.func, ast.Attribute) and 
                isinstance(node.value.func.value, ast.Name) and 
                node.value.func.value.id == "env" and 
                node.value.func.attr == "get_sensor_forward_value"):
                sensor_variable = node.targets[0].id 

    if not sensor_variable:
        issues.append({
            "message": "No variable found assigned from `env.get_sensor_forward_value()`. Check a sensor value is stored.",
            "line": 1  
        })
        return issues  

    while_found = False
    variable_used_in_condition = False
    variable_updated_inside_loop = False

    for node in ast.walk(tree):
        if isinstance(node, ast.While):
            while_found = True
           
            if isinstance(node.test, ast.Compare) and isinstance(node.test.left, ast.Name):
                if node.test.left.id == sensor_variable:
                    variable_used_in_condition = True

            for child in ast.walk(node):
                if isinstance(child, ast.Assign) and isinstance(child.value, ast.Call):
                    if (isinstance(child.value.func, ast.Attribute) and 
                        isinstance(child.value.func.value, ast.Name) and 
                        child.value.func.value.id == "env" and 
                        child.value.func.attr == "get_sensor_forward_value"):
                        if isinstance(child.targets[0], ast.Name) and child.targets[0].id == sensor_variable:
                            variable_updated_inside_loop = True

    if not while_found:
        issues.append({
            "message": "No `while` loop found using a sensor variable. Check the loop correctly waits for an object detection.",
            "line": 1
        })
    elif not variable_used_in_condition:
        issues.append({
            "message": f"While loop condition does not correctly use `{sensor_variable}` assigned from `env.get_sensor_forward_value()`. Check the condition is based on this sensor value.",
            "line": 1
        })
    elif not variable_updated_inside_loop:
        issues.append({
            "message": f"Inside the while loop, `{sensor_variable}` is not updated from `env.get_sensor_forward_value()`. Check it is re-assigned inside the loop.",
            "line": 1
        })

    return issues

def check_ascend_action_in_correct_for_loop_sensors(tree):
    """Check that the ascend action value is correctly applied to the environment."""
    issues = []

    for node in ast.walk(tree):
        if isinstance(node, ast.For):  
           
            if (isinstance(node.iter, ast.Call) and
                isinstance(node.iter.func, ast.Name) and
                node.iter.func.id == "range" and
                len(node.iter.args) == 1 and
                isinstance(node.iter.args[0], ast.Constant) and
                node.iter.args[0].value == 40):
                ascend_action_found = False
                for child in ast.walk(node):
                    if isinstance(child, ast.Expr) and isinstance(child.value, ast.Call):
                        func = child.value.func
                        if (isinstance(func, ast.Attribute) and
                            isinstance(func.value, ast.Name) and func.value.id == "env" and
                            func.attr == "step" and
                            len(child.value.args) > 0 and
                            isinstance(child.value.args[0], ast.Name) and
                            child.value.args[0].id == "ascend_action"):
                            ascend_action_found = True  

              
                contains_ascend_comment = any(
                    isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Str) and 
                    "Apply the ascend action to the environment" in stmt.value.s
                    for stmt in node.body
                )

                if contains_ascend_comment and not ascend_action_found:
                    issues.append({
                        "message": "Missing `env.step(ascend_action)` inside the `for _ in range(40):` loop.",
                        "line": node.lineno
                    })

    return issues

# ---------------- Static Analysis Functions for AUTONOMOUS CAR ROBOT -------------------------#
def check_sensor_forward_value_retrieval_car(tree):
    """Check that `env.get_sensor_forward_value()` is called inside of the infinite while loop and that its return value is stored in a variable."""
    issues = []
    last_line_number = 1
    forward_sensor_called = False
    forward_sensor_assigned = False
    inside_while_true_loop = False

    for node in ast.walk(tree):
        if hasattr(node, "lineno"):
            last_line_number = node.lineno  

        if isinstance(node, ast.While):
            if isinstance(node.test, ast.Constant) and node.test.value is True:
                inside_while_true_loop = True

        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name) and node.func.value.id == "env":
                if node.func.attr == "get_sensor_forward_value":
                    forward_sensor_called = True

        if isinstance(node, ast.Assign):
            if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute):
                if (isinstance(node.value.func.value, ast.Name) and 
                    node.value.func.value.id == "env" and 
                    node.value.func.attr == "get_sensor_forward_value"):
                    forward_sensor_assigned = True

    if inside_while_true_loop and forward_sensor_called and not forward_sensor_assigned:
        issues.append({
            "message": "The return value of `env.get_sensor_forward_value()` should be stored in a variable.",
            "line": last_line_number
        })

    if inside_while_true_loop and not forward_sensor_called:
        issues.append({
            "message": "Missing call to `env.get_sensor_forward_value()`. This function needs to be called inside the infinite while loop to retrieve the forward sensor value of the car.",
            "line": last_line_number
        })

    return issues

def check_sensor_right_value_retrieval_car(tree):
    """Check that `env.get_sensor_right_value()` is called inside of the infinite while loop and that its return value is stored in a variable."""
    issues = []
    last_line_number = 1
    right_sensor_called = False
    right_sensor_assigned = False
    inside_while_true_loop = False

    for node in ast.walk(tree):
        if hasattr(node, "lineno"):
            last_line_number = node.lineno  

        if isinstance(node, ast.While):
            if isinstance(node.test, ast.Constant) and node.test.value is True:
                inside_while_true_loop = True

        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name) and node.func.value.id == "env":
                if node.func.attr == "get_sensor_right_value":
                    right_sensor_called = True

        if isinstance(node, ast.Assign):
            if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute):
                if (isinstance(node.value.func.value, ast.Name) and 
                    node.value.func.value.id == "env" and 
                    node.value.func.attr == "get_sensor_right_value"):
                    right_sensor_assigned = True

    if inside_while_true_loop and right_sensor_called and not right_sensor_assigned:
        issues.append({
            "message": "The return value of `env.get_sensor_right_value()` should be stored in a variable.",
            "line": last_line_number
        })

    if inside_while_true_loop and not right_sensor_called:
        issues.append({
            "message": "Missing call to `env.get_sensor_right_value()`. This function needs to be called inside the infinite while loop to retrieve the right sensor value for the car.",
            "line": last_line_number
        })

    return issues

def check_sensor_left_value_retrieval_car(tree):
    """Check that `env.get_sensor_left_value()` is called inside of the infinite while loop and that its return value is stored in a variable."""
    issues = []
    last_line_number = 1
    left_sensor_called = False
    left_sensor_assigned = False
    inside_while_true_loop = False

    for node in ast.walk(tree):
        if hasattr(node, "lineno"):
            last_line_number = node.lineno  

        if isinstance(node, ast.While):
            if isinstance(node.test, ast.Constant) and node.test.value is True:
                inside_while_true_loop = True

        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name) and node.func.value.id == "env":
                if node.func.attr == "get_sensor_left_value":
                    left_sensor_called = True

        if isinstance(node, ast.Assign):
            if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute):
                if (isinstance(node.value.func.value, ast.Name) and 
                    node.value.func.value.id == "env" and 
                    node.value.func.attr == "get_sensor_left_value"):
                    left_sensor_assigned = True

    if inside_while_true_loop and left_sensor_called and not left_sensor_assigned:
        issues.append({
            "message": "The return value of `env.get_sensor_left_value()` should be stored in a variable.",
            "line": last_line_number
        })

    if inside_while_true_loop and not left_sensor_called:
        issues.append({
            "message": "Missing call to `env.get_sensor_left_value()`. This function needs to be called inside the infinite while loop to retrieve the left sensor value for the car.",
            "line": last_line_number
        })

    return issues


def check_sensor_readings_variable_usage_car(tree):
    """Check that the correct sensor variables are used in the `sensor_readings` dictionary"""
    issues = []
    last_line_number = 1
    
    sensor_variables = {
        "Forward": None,
        "Right": None,
        "Left": None
    }

    for node in ast.walk(tree):
        if hasattr(node, "lineno"):
            last_line_number = node.lineno  

        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Attribute) and isinstance(node.value.func.value, ast.Name):
                if node.value.func.value.id == "env":
                    if node.value.func.attr == "get_sensor_forward_value":
                        sensor_variables["Forward"] = node.targets[0].id
                    elif node.value.func.attr == "get_sensor_right_value":
                        sensor_variables["Right"] = node.targets[0].id
                    elif node.value.func.attr == "get_sensor_left_value":
                        sensor_variables["Left"] = node.targets[0].id

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Dict):
            if isinstance(node.targets[0], ast.Name) and node.targets[0].id == "sensor_readings":
                keys = [k.s for k in node.value.keys if isinstance(k, ast.Str)]  
                values = [v.id if isinstance(v, ast.Name) else None for v in node.value.values] 

                for key in sensor_variables:
                    if key in keys:
                        index = keys.index(key)
                        assigned_var = values[index]

                        if assigned_var is None:
                            issues.append({
                                "message": f"The `{key}` sensor reading is missing a value in `sensor_readings`. Please assign a variable.",
                                "line": node.lineno
                            })
                        elif assigned_var != sensor_variables[key]:
                            issues.append({
                                "message": f"The `{key}` sensor reading should use the variable `{sensor_variables[key]}`, but `{assigned_var}` was used instead.",
                                "line": node.lineno
                            })
                    else:
                        issues.append({
                            "message": f"The `{key}` sensor reading is missing from `sensor_readings`. Check to include all sensor readings.",
                            "line": node.lineno
                        })

    return issues

def check_dictionary_key_safety_car(tree):
    """Check if dictionary key accesses are safe."""
    issues = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name) and isinstance(node.slice, ast.Constant):
            dict_name = node.value.id
            key_name = node.slice.value
            if dict_name == "values" and key_name not in {"Forward", "Right", "Left"}:
                issues.append({
                    "message": f"Possible unsafe dictionary lookup: '{key_name}' not guaranteed to exist.",
                    "line": node.lineno
                })
    return issues

# def check_max_direction_usage_car(tree):
#     """Check that a variable is assigned using `max(sensor_readings, key=sensor_readings.get)` correctly."""
#     issues = []
#     last_line_number = 1
#     found_max_usage = False

#     for node in ast.walk(tree):
#         if hasattr(node, "lineno"):
#             last_line_number = node.lineno  

#         if isinstance(node, ast.Assign):
#             if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == "max":
#                 if len(node.value.args) > 0 and isinstance(node.value.args[0], ast.Name) and node.value.args[0].id == "sensor_readings":
#                     for keyword in node.value.keywords:
#                         if keyword.arg == "key" and isinstance(keyword.value, ast.Attribute):
#                             if (
#                                 isinstance(keyword.value.value, ast.Name)
#                                 and keyword.value.value.id == "sensor_readings"
#                                 and keyword.value.attr == "get"
#                             ):
#                                 found_max_usage = True
#                                 break

#     if not found_max_usage:
#         issues.append({
#             "message": "A variable must be assigned using `max(sensor_readings, key=sensor_readings.get)`. Check `max()` is applied correctly.",
#             "line": last_line_number
#         })

#     return issues


def check_max_direction_usage_car(tree):
    """Check that a variable is assigned using `max(sensor_readings, key=sensor_readings.get)` correctly, regardless of variable name."""
    issues = []
    last_line_number = 1
    found_max_usage = False
    assigned_variable_name = None 
    first_missing_reference = None  

    for node in ast.walk(tree):
        if hasattr(node, "lineno"):
            last_line_number = node.lineno  

        if isinstance(node, ast.Assign):
            if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == "max":
                if len(node.value.args) > 0 and isinstance(node.value.args[0], ast.Name) and node.value.args[0].id == "sensor_readings":
                    for keyword in node.value.keywords:
                        if keyword.arg == "key" and isinstance(keyword.value, ast.Attribute):
                            if (
                                isinstance(keyword.value.value, ast.Name)
                                and keyword.value.value.id == "sensor_readings"
                                and keyword.value.attr == "get"
                            ):
                                if isinstance(node.targets[0], ast.Name):
                                    assigned_variable_name = node.targets[0].id
                                    found_max_usage = True
                                break 

        if isinstance(node, ast.Name):
            if assigned_variable_name is None and first_missing_reference is None:
                first_missing_reference = node.lineno 

    if not found_max_usage and first_missing_reference is not None:
        issues.append({
            "message": "A variable must be assigned using `max(sensor_readings, key=sensor_readings.get)`. Check `max()` is applied correctly.",
            "line": first_missing_reference 
        })

    return issues

def check_if_else_with_greatest_direction_car(tree):
    """Check that the variable assigned with `max(sensor_readings, key=sensor_readings.get)` is the same variable used in the if-else conditions."""
    issues = []
    last_line_number = 1
    max_variable = None  

    for node in ast.walk(tree):
        if hasattr(node, "lineno"):
            last_line_number = node.lineno  

        if isinstance(node, ast.Assign):
            if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == "max":
                if len(node.value.args) > 0 and isinstance(node.value.args[0], ast.Name) and node.value.args[0].id == "sensor_readings":
                    for keyword in node.value.keywords:
                        if keyword.arg == "key" and isinstance(keyword.value, ast.Attribute):
                            if (
                                isinstance(keyword.value.value, ast.Name)
                                and keyword.value.value.id == "sensor_readings"
                                and keyword.value.attr == "get"
                            ):
                                max_variable = node.targets[0].id 

    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            if isinstance(node.test, ast.Compare):
                if isinstance(node.test.left, ast.Name):
                    condition_variable = node.test.left.id  

                    # if max_variable is None:
                    #     issues.append({
                    #         "message": "A variable must be assigned using `max(sensor_readings, key=sensor_readings.get)` before the if-else statement.",
                    #         "line": node.lineno
                    #     })
                    if condition_variable != max_variable:
                        issues.append({
                            "message": f"The if-else statement should use `{max_variable}`, but `{condition_variable}` was used instead.",
                            "line": node.lineno
                        })

    return issues

def check_env_step_usage_car(tree):
    """Check that `env.step(action)` is called inside the while loop and that `action` is used as the argument."""
    issues = []
    last_line_number = 1
    step_called_correctly = False
    step_called_incorrectly = False

    for node in ast.walk(tree):
        if hasattr(node, "lineno"):
            last_line_number = node.lineno  

        if (
            isinstance(node, ast.Call) and 
            isinstance(node.func, ast.Attribute) and 
            isinstance(node.func.value, ast.Name)  
        ):
            if node.func.value.id == "env" and node.func.attr == "step":
                if len(node.args) > 0 and isinstance(node.args[0], ast.Name):
                    if node.args[0].id == "action":
                        step_called_correctly = True  
                    else:
                        step_called_incorrectly = True 

    if not step_called_correctly:
        issues.append({
            "message": "Missing required call to `env.step(action)` is missing. The simulation may not function correctly. Check that it is called inside the infinite loop to execute movement.",
            "line": last_line_number
        })

    if step_called_incorrectly:
        issues.append({
            "message": "Incorrect argument passed to `env.step()`. Check that only `action` is used as the argument.",
            "line": last_line_number
        })

    return issues

def check_undefined_variables_car(tree):
    issues = []
    defined_vars = set()
    used_vars = set()
    last_line_number = 1  

    for node in ast.walk(tree):
        if hasattr(node, "lineno"):  
            last_line_number = node.lineno  

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    defined_vars.add(target.id)
        elif isinstance(node, ast.Name):
            used_vars.add(node.id)

    assumed_defined_vars = {"env", "time", "max", "np", "contact"}
    undefined_vars = used_vars - defined_vars - assumed_defined_vars

    for var in undefined_vars:
        issues.append({
            "message": f"Variable '{var}' is used but not defined.",
            "line": last_line_number  
        })

    return issues

def analyze_robotics_code(code, context="Car"):
    """Analyze code for robotics-specific logical issues."""
    issues = []
    print(f"Analyzing code in context: {context}")
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        # Do not include syntax errors in static issues.
        return issues

    if context == "Fetch Reach":
        issues.extend(check_object_transport_fetch_reach(tree))
        issues.extend(check_ball_position_retrieval_fetch_reach(tree))
        issues.extend(check_gripper_position_retrieval_fetch_reach(tree))
        issues.extend(check_direction_computation_fetch_reach(tree))
        issues.extend(check_np_array_wrapping_fetch_reach(tree))
        issues.extend(check_direction_normalization_fetch_reach(tree))
        issues.extend(check_for_loop_usage_fetch_reach(tree))
        issues.extend(check_loop_termination_fetch_reach(tree))
        issues.extend(check_while_loop_normalized_comparison_fetch_reach(tree))
    elif context == "Fetch Pick and Place":
        issues.extend((tree))
    elif context == "Fetch Organize":
        issues.extend(check_undefined_variables_fetch_organize(tree))
        issues.extend(check_site_xpos_object_name_usage_twice_fetch_organize(tree))
        issues.extend(check_site_xpos_robot_grip_usage_three_times_fetch_organize(tree))
        issues.extend(check_opens_gripper_first_fetch_organize(tree))
        issues.extend(check_env_step_usage_in_while_loops_fetch_organize(tree))
        issues.extend(check_closes_gripper_after_vertical_fetch_organize(tree))
        issues.extend(check_horizontal_distance_subtraction_fetch_organize(tree))
    elif context == "Fetch Sensors":
        issues.extend(check_one_env_step_sensors(tree))
        issues.extend(check_loop_termination_sensors(tree))
        issues.extend(check_forward_sensor_value_assignment_sensors(tree))
        issues.extend(check_while_loop_sensor_condition_sensors(tree))
        issues.extend(check_ascend_action_in_correct_for_loop_sensors(tree))
    elif context == "Car": 
        issues.extend(check_sensor_forward_value_retrieval_car(tree))
        issues.extend(check_sensor_right_value_retrieval_car(tree))
        issues.extend(check_sensor_left_value_retrieval_car(tree))
        issues.extend(check_sensor_readings_variable_usage_car(tree))
        issues.extend(check_dictionary_key_safety_car(tree))
        issues.extend(check_max_direction_usage_car(tree))
        issues.extend(check_if_else_with_greatest_direction_car(tree))
        issues.extend(check_env_step_usage_car(tree))
        issues.extend(check_undefined_variables_car(tree))
      
    return issues


logs_db = {}  

def log_event(user_id, page_context, code, static_issues, error, hints):
    """Stores a log entry for a given user_id."""
    entry = {
        "timestamp": datetime.now(),
        "page_context": page_context,
        "code": code,
        "static_issues": static_issues,
        "error": error,
        "hints": hints
    }
    logs_db.setdefault(user_id, []).append(entry)

    # Convert dictionaries/lists to JSON strings before storing
    static_issues_str = json.dumps(static_issues) if static_issues else None
    hints_str = json.dumps(hints) if hints else None
    error_str = json.dumps(error) if isinstance(error, (dict, list)) else error

    new_log = UserCodeLogs(
        user_id=user_id,
        page_context=page_context,
        code=code,
        static_issues=static_issues_str,
        error=error_str,
        hints=hints_str,
        created_at=datetime.utcnow()
    )

    db.session.add(new_log)
    db.session.commit()

@app.route('/chatbot-api', methods=['POST'])
def ChatbotAPI():
    print("Chatbot API called")
    global user_submitted_code
    global last_error
    global static_issues
    global last_error_line
    global hint_level

    user = session.get('user')
    if not user:
        return jsonify({'error': 'You must be logged in to use the chatbot API.'}), 401

    user_id = user['user_id']

    if 'last_error_line' not in globals():
        last_error_line = None
    if 'hint_level' not in globals():
        hint_level = 1

    data = request.get_json()

    if not data:
        print("ERROR: No JSON data received in request!")
        return jsonify({'error': 'No JSON data received!'}), 400

    print("Received JSON data", data)  
    page_context = data.get('page_context')

    print("Extracted page_context from request", page_context)

    page_contexts = {
        "/Fetch-Reach-Robot": "Fetch Reach",
        "/PickAndPlacePage": "Fetch Pick and Place",
        "/FetchStackPage": "Fetch Stack",
        "/FetchOrganizePage": "Fetch Organize",
        "/FetchOrganizeSensorsPage": "Fetch Sensors",
        "/CarPage": "Car", 
    }

    if not page_context or page_context == "General":
        current_path = request.headers.get('Referer', request.path) 
        page_context = page_contexts.get(current_path, "General")

    print(f"Final Page Context Used {page_context}")

    error_line = data.get('error_line')  
    error_message = data.get('error_message')
    print(f"Received Error Line: {error_line}, Last Error Line: {last_error_line}")
    print(f"Current Hint Level: {hint_level}, Error Message: {error_message}")

    if error_line != last_error_line:
        hint_level = 1
        last_error_line = error_line
    else:
        hint_level += 1

    if static_issues:
        static_issues_text = "\n".join(
            f"Line {issue['line']}: {issue['message']}"
            for issue in static_issues
            if isinstance(issue, dict)
        )
    else:
        static_issues_text = "None"

    if static_issues and last_error:
        focus = "Focus on syntax errors first, then address the following static issues."
    elif static_issues:
        focus = "Focus on the following static issues."
    elif last_error:
        focus = "Focus on resolving the syntax error below."
    else:
        return jsonify({'reply': "No errors or static issues detected. Your code looks good!"})

    # Construct prompt using stored code
    prompt = f"""
    You are a helpful chatbot. Based on the current hint level ({hint_level}), provide guidance:
    - Level 1: General guidance.
    - Level 2: More specific guidance.
    - Level 3: Precise, actionable advice.
    - Level 4: In-depth explanation and direct solution.

    {focus}

    Syntax Error:
    {last_error or 'None'}

    Static Issues:
    {static_issues_text}

    User Code:
    {user_submitted_code}

    Provide a single hint matching the specificity level ({hint_level}). 
    This is the format for your response:
    "HINTS:\n"
    "1. Hint text here."
    """

    print("Constructed Prompt:\n", prompt)

    # 4) Call the Gemini API (or your LLM)
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
        response = requests.post(
            f"{api_url}?key={api_key}",
            headers={'Content-Type': 'application/json'},
            json=payload
        )
        print("API Response:", response.text)

        if response.status_code != 200:
            return jsonify({'error': f'Error from API: {response.text}'}), 500

        response_json = response.json()
        if 'candidates' in response_json and len(response_json['candidates']) > 0:
            chatbot_response = (
                response_json['candidates'][0]
                .get('content', {})
                .get('parts', [{}])[0]
                .get('text', 'No response')
            )
        else:
            chatbot_response = 'No contents available in the response'

    except Exception as e:
        print("Error occurred:", e)
        return jsonify({'error': str(e)}), 500

    hints = []
    if "HINTS:" in chatbot_response:
        hints_section = chatbot_response.split("HINTS:")[-1].strip()
        hints = [hint.strip() for hint in hints_section.split("\n") if hint.strip()]

    log_event(
        user_id=user_id,
        page_context=page_context,
        code=user_submitted_code,
        static_issues=static_issues,
        error=last_error,
        hints=hints
    )

    print("Logging the event after hints......")
    print("Current logs for this user:", logs_db.get(user_id, []))

    print("Extracted Hints:", hints)

    return jsonify({
        'reply': chatbot_response,
        'hints': hints[:1]
    })

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

        if not check_password_requirements(password):
            return render_template('account/signup.html', is_homepage=True)
        
        if not is_valid_email(email):
            flash("Invalid Email Address")
            return render_template('account/signup.html', is_homepage=True)

        new_user = User()

        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.email = email
        new_user.username = username
        new_user.password = hash_password(password)
        if account_type == 'instructor':
            new_user.role_id = 1
        elif account_type == 'student':
            new_user.role_id = 2

        if not check_default_values(new_user):
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

            if new_user.role_id == 2:
                default_courses_name = [
                    "Introduction to Robotics",
                    "Types of Robots",
                    "Robots in CORE",
                    "How to Use the Lab"
                ]
                for course_name in default_courses_name:
                    course = Courses.query.filter_by(course_name=course_name).first()
                    if course:
                        student_assignment = StudentAssignedCourses(
                            user_id=new_user.user_id,
                            course_id=course.course_id
                        )
                        db.session.add(student_assignment)

                        section_number = course.section_number
                        subsections = CourseSubsections.query.filter(
                            CourseSubsections.course_subsection_number > section_number,
                            CourseSubsections.course_subsection_number < section_number + 1
                        ).all()
                        for subsection in subsections:
                            student_subsection_assignment = StudentAssignedCourseSubsections(user_id=new_user.user_id, course_subsection_number=subsection.course_subsection_number)
                            db.session.add(student_subsection_assignment)

                db.session.commit()

            if new_user.role_id == 1:
                return redirect(url_for('RenderInstructorDashboard'))
            elif new_user.role_id == 2:
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
                elif role == ROLE_ADMIN:
                    return redirect(url_for('RenderAdminDashboard'))
            else:
                flash('Invalid Password', 'error')
        else:
            flash('Invalid Username', 'error')
    return render_template('account/login.html', is_homepage=True)

@app.route('/forgot-password', methods=['GET', 'POST'])
def RenderForgotPassword():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        
        # Verify user exists and email matches
        success, user = get_user(username)
        if success and user.email.lower() == email.lower():  # Case-insensitive comparison
            # Create reset link with encoded email
            encoded_email = quote(email)  # URL-encode the email
            password_reset_link = url_for('RenderResetPassword', email=encoded_email, _external=True)
            
            # Send email
            subject = "CORE - Reset Password"
            body = render_template("account/forgot_password.txt", 
                                 username=username, 
                                 password_reset_link=password_reset_link)
            send_email(subject, email, body)
        
        # Always show success to prevent email enumeration
        flash("If an account exists with that username/email, we've sent a password reset link.", "success")
        return redirect(url_for('RenderForgotPassword'))
    
    return render_template('account/forgot_password.html', is_homepage=True)

@app.route('/reset-password/<email>', methods=['GET', 'POST'])
def RenderResetPassword(email):
    try:
        # Decode the email address
        email = unquote(email)
        
        # Basic validation - check if email exists in your system
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Invalid password reset link.", "error")
            return redirect(url_for('RenderForgotPassword'))

    except:
        flash("Invalid password reset link.", "error")
        return redirect(url_for('RenderForgotPassword'))

    if request.method == 'POST':
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if new_password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(request.url)  # Stay on same page
        
        # Update the user's password
        user.password = hash_password(new_password)
        db.session.commit()
        
        flash("Password has been reset successfully.", "success")
        return redirect(url_for('RenderLogin'))
    
    return render_template('account/reset_password.html', email=email, is_homepage=True)

@app.route('/dashboard/admin-view/home', methods=['GET', 'POST'])
def RenderAdminDashboard():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.', 'popup')
        return redirect(url_for('RenderHomepage'))

    user_id = user['user_id'] 
    role = user['role_id']
    
    if role != ROLE_ADMIN:
        flash('You have insufficient permissions to access this page.', 'popup')
        return redirect(url_for('RedirectUser'))

    role_name = Roles.query.filter_by(role_id=role).first().role_name

    recent_users = (
        User.query
        .order_by(User.created_at.desc())
        .limit(10)
        .all()
    )

    # Query recent class creations (last 10 classes)
    recent_classes = (
        Classes.query
        .order_by(Classes.created_at.desc())
        .limit(10)
        .all()
    )

    # Combine and sort the activities by creation date
    recent_activities = []
    for user in recent_users:
        recent_activities.append({
            'type': 'user',
            'name': user.username,  # Assuming 'username' is a field in the User model
            'created_at': user.created_at  # This is already a datetime.datetime object
        })

    for class_ in recent_classes:
        # Construct the class name using class_course_code and section_number
        class_name = f"{class_.class_course_code} - Section {class_.class_section_number}"

        # Convert date to datetime by adding a time component (00:00:00)
        class_created_at = datetime.combine(class_.created_at, datetime_time.min)  # Use datetime.time.min
        recent_activities.append({
            'type': 'class',
            'name': class_name,  # Use the constructed class name
            'created_at': class_created_at  # Now a datetime.datetime object
        })

    # Sort activities by creation date (most recent first)
    recent_activities.sort(key=lambda x: x['created_at'], reverse=True)

    # Calculate the date 7 days ago from today
    one_week_ago = datetime.utcnow() - timedelta(days=7)

    # Query the number of users who joined each day for the past week
    users_per_day = (
        db.session.query(
            func.date(User.created_at).label('date'),
            func.count(User.user_id).label('count')
        )
        .filter(User.created_at >= one_week_ago)
        .group_by(func.date(User.created_at))
        .order_by(func.date(User.created_at))
        .all()
    )

    # Query the number of classes created each day for the past week
    classes_per_day = (
        db.session.query(
            func.date(Classes.created_at).label('date'),
            func.count(Classes.class_id).label('count')
        )
        .filter(Classes.created_at >= one_week_ago)
        .group_by(func.date(Classes.created_at))
        .order_by(func.date(Classes.created_at))
        .all()
    )

    # Generate a list of dates for the past 7 days
    date_range = [(datetime.utcnow() - timedelta(days=i)).date() for i in range(6, -1, -1)]

    # Convert query results into dictionaries for easy lookup
    users_per_day_dict = {row.date: row.count for row in users_per_day}
    classes_per_day_dict = {row.date: row.count for row in classes_per_day}

    # Merge with the date range, defaulting to 0 for missing dates
    complete_data = []
    for date in date_range:
        user_count = users_per_day_dict.get(date, 0)  # Default to 0 if the date is not in the query results
        class_count = classes_per_day_dict.get(date, 0)  # Default to 0 if the date is not in the query results
        complete_data.append((date.strftime('%Y-%m-%d'), user_count, class_count))

    # Separate dates, user counts, and class counts
    dates = [item[0] for item in complete_data]
    user_counts = [item[1] for item in complete_data]
    class_counts = [item[2] for item in complete_data]

    # Generate the graph using Matplotlib
    plt.figure(figsize=(10, 5))

    # Plot users data
    plt.plot(dates, user_counts, marker='o', linestyle='-', color='b', label='Users Joined')

    # Plot classes data
    plt.plot(dates, class_counts, marker='s', linestyle='--', color='r', label='Classes Created')

    # Add title, labels, and legend
    plt.title('Users and Classes Created Per Day (Last 7 Days)')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.grid(True)
    plt.legend()  # Show legend to differentiate between users and classes

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    # Encode the image to base64 for embedding in HTML
    graph_image = base64.b64encode(buf.read()).decode('utf-8')

    # Other stats
    since_date = datetime(2025, 2, 24)
    total_users = User.query.count()
    users_since = User.query.filter(User.created_at >= since_date).count()

    total_classes = Classes.query.count()
    classes_since = Classes.query.filter(Classes.created_at >= since_date).count()

    users_stats = {
        'total_users': total_users,
        'users_since': users_since,
        'since_date': since_date,
        'graph_image': graph_image
    }

    classes_stats = {
        'total_classes': total_classes,
        'classes_since': classes_since,
        'since_date': since_date
    }

    return render_template('dashboard/admin/dashboard_admin.html', 
                           is_dashboard=True, 
                           is_admin_dashboard=True, 
                           users_stats=users_stats, 
                           classes_stats=classes_stats,
                           recent_activities=recent_activities,
                           user=user,
                           role_name=role_name)

@app.route('/dashboard/admin-view/user-list', methods=['GET', 'POST'])
def RenderAdminUserList():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.', 'popup')
        return redirect(url_for('RenderHomepage'))

    user_id = user['user_id'] 
    role = user['role_id']
    
    if role != ROLE_ADMIN:
        flash('You have insufficient permissions to access this page.', 'popup')
        return redirect(url_for('RedirectUser'))

    role_name = Roles.query.filter_by(role_id=role).first().role_name

    registered_users = db.session.query(User).join(Roles).order_by(Roles.role_name).all()
    return render_template('dashboard/admin/dashboard_admin_user_list.html', 
                            is_dashboard=True, 
                            is_admin_dashboard=True, 
                            registered_users=registered_users, 
                            selected_user=None,
                            user=user,
                            role_name=role_name)

@app.route('/dashboard/admin/update-user', methods=['POST'])
def update_user():
    user_id = request.form.get('user_id')
    new_role_id = request.form.get('role_id')
    new_first_name = request.form.get('first_name')
    new_last_name = request.form.get('last_name')
    new_email = request.form.get('email')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    print(new_email)

    if not user_id:
        flash("Invalid request.", 'popup')
        return redirect(url_for('RenderAdminUserList'))

    user = User.query.get(user_id)
    if not user:
        flash("User not found.", 'popup')
        return redirect(url_for('RenderAdminUserList'))

    try:
        # Update role if changed
        if new_role_id:
            role = Roles.query.get(new_role_id)
            if role:
                user.role_id = new_role_id
            else:
                flash("Invalid role.", 'popup')

        # Update name
        if new_first_name and new_last_name:
            user.first_name = new_first_name
            user.last_name = new_last_name

        # Update email
        if new_email and is_valid_email(new_email):
            user.email = new_email
        else:
            flash("Invalid Email Address", 'popup')

        # Update password (if provided)
        if new_password:
            if new_password == confirm_password and check_password_requirements(new_password):
                user.password = hash_password(new_password)
            else:
                flash("Passwords do not match or do not meet security requirements.", 'popup')

        # Commit changes
        db.session.commit()
        flash("User updated successfully.", 'popup')

    except Exception as e:
        db.session.rollback()
        flash(f"Error: {str(e)}", 'popup')

    return redirect(url_for('RenderAdminUserList'))

@app.route('/dashboard/admin/remove-user', methods=['POST'])
def remove_user():
    user_id = request.form.get('user_id')

    if not user_id:
        flash("Invalid request.", 'popup')
        return redirect(url_for('RenderAdminUserList'))

    user = User.query.get(user_id)

    if not user:
        flash("User not found.", 'popup')
        return redirect(url_for('RenderAdminUserList'))

    try:
        db.session.delete(user)
        db.session.commit()
        flash("User removed successfully.", 'popup')
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {str(e)}", 'popup')

    return redirect(url_for('RenderAdminUserList'))
    
@app.route('/dashboard/admin-view/classes', methods=['GET', 'POST'])
def RenderAdminClassesList():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.', 'popup')
        return redirect(url_for('RenderHomepage'))

    user_id = user['user_id'] 
    role = user['role_id']
    
    if role != ROLE_ADMIN:
        flash('You have insufficient permissions to access this page.', 'popup')
        return redirect(url_for('RedirectUser'))

    role_name = Roles.query.filter_by(role_id=role).first().role_name

    registered_classes = db.session.query(Classes).all()

    class_data = []
    instructors = db.session.query(User).filter_by(role_id=ROLE_INSTRUCTOR).all()  # Fetch all instructors

    for classes in registered_classes:
        course_info = f"{classes.class_course_code} - Section {classes.class_section_number}"

        student_count = db.session.query(Enrollment).filter_by(class_id=classes.class_id).count()

        instructor = db.session.query(User).filter_by(user_id=classes.user_id).first()
        instructor_name = f"{instructor.first_name} {instructor.last_name}" if instructor else "No Instructor"

        class_data.append({
            'class_id': classes.class_id,
            'course_info': course_info,
            'student_count': student_count,
            'instructor_id': classes.user_id,
            'instructor_name': instructor_name
        })

    return render_template(
        'dashboard/admin/dashboard_admin_classes_list.html',
        is_dashboard=True,
        is_admin_dashboard=True,
        class_data=class_data,
        instructors=instructors,
        user=user,
        role_name=role_name)


@app.route('/dashboard/classes/remove_class', methods=['POST'])
def remove_class():
    class_id = request.form.get('class_id')

    if not class_id:
        flash("Invalid request: Missing class ID.", 'popup')
        return redirect(url_for('RenderAdminClassesList'))

    class_to_remove = Classes.query.get(class_id)

    if not class_to_remove:
        flash("Class not found.", 'popup')
        return redirect(url_for('RenderAdminClassesList'))

    try:
        # Delete all related class_codes entries
        ClassCodes.query.filter_by(class_id=class_id).delete()

        # Now delete the class
        db.session.delete(class_to_remove)
        db.session.commit()
        flash("Class removed successfully.", 'popup')
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {str(e)}", 'popup')

    return redirect(url_for('RenderAdminClassesList'))

@app.route('/dashboard/classes/change_class_name', methods=['POST'])
def change_class_name():
    class_id = request.form.get('class_id')  # Use class_id to find the class
    class_course_code = request.form.get('class_course_code')  # Get the new class course code
    class_section_number = request.form.get('class_section_number')  # Get the new class section number

    # Check if class_id is provided
    if not class_id:
        flash("Invalid request: Missing class ID.", 'popup')
        return redirect(url_for('RenderAdminClassesList'))

    # Find the class by class_id
    class_to_update = Classes.query.get(class_id)

    if not class_to_update:
        flash("Class not found.", 'popup')
        return redirect(url_for('RenderAdminClassesList'))

    try:
        # Update the course code and section number
        if class_course_code:
            class_to_update.class_course_code = class_course_code
        
        if class_section_number:
            class_to_update.class_section_number = class_section_number
        
        # Update the class_name by combining the new course code and section number
        class_to_update.class_name = f"{class_to_update.class_course_code} - {class_to_update.class_section_number}"

        db.session.commit()
        flash("Class updated successfully.", 'popup')
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {str(e)}", 'popup')

    return redirect(url_for('RenderAdminClassesList'))



@app.route('/dashboard/classes/change-class-instructor', methods=['POST'])
def change_class_instructor():
    class_id = request.form.get('class_id')
    new_instructor_id = request.form.get('instructor_id')

    if not class_id or not new_instructor_id:
        flash("Invalid request.", 'popup')
        return redirect(url_for('RenderAdminUserList'))

    cls = Classes.query.get(class_id)
    instructor = User.query.get(new_instructor_id)

    if not cls:
        flash("Class not found.", 'popup')
        return redirect(url_for('RenderAdminUserList'))

    if not instructor:
        flash("Instructor not found.", 'popup')
        return redirect(url_for('RenderAdminUserList'))

    try:
        cls.user_id = new_instructor_id
        db.session.commit()
        flash("Class instructor updated successfully.", 'popup')
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {str(e)}", 'popup')

    return redirect(url_for('RenderAdminUserList'))

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
        'dashboard/instructor/dashboard_class_details.html',
        is_dashboard=True,
        is_instructor_dashboard=True,
        students=students
    )

@app.route('/dashboard/student-view', methods=['GET', 'POST'])
def RenderStudentDashboard():
    course_id = request.args.get('course_id')
    completed = request.args.get('completed')

    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))

    user_id = user['user_id'] 
    role = user['role_id']
    
    if (role != ROLE_STUDENT):
        flash('You must be an student to access this page.', 'popup')
        return redirect(url_for('RedirectUser'))
    
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
        
    course_completed_info = None
    if completed and course_id:
        course = Courses.query.get(course_id)
        if course:
            course_completed_info = {
                'course_name': course.course_name,
                'completed': True
            }

    existing_enrollment = Enrollment.query.filter_by(user_id=user_id).first()
    in_class = existing_enrollment is not None

    assignments = db.session.query(StudentAssignedCourses).filter(StudentAssignedCourses.user_id == user_id).all()

    return render_template('dashboard/student/dashboard_student.html', is_dashboard=True, is_student_dashboard=True, user=user, assignments=assignments, in_class=in_class,
                           course_completed_info=course_completed_info)

@app.route('/dashboard/student-view/grades', methods=['GET', 'POST'])
def RenderStudentDashboardGrades():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))

    user_id = user['user_id'] 
    role = user['role_id']
    
    if (role != ROLE_STUDENT):
        flash('You must be an student to access this page.', 'popup')
        return redirect(url_for('RedirectUser'))
    
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

    grades = db.session.query(
        StudentGrades.course_subsection_id,
        db.func.max(StudentGrades.percentage_grade).label('highest_grade')
    ).filter(
        StudentGrades.student_id == user_id
    ).group_by(
        StudentGrades.course_subsection_id
    ).all()

    # Fetch course subsection names and course names
    grades_with_names = []
    for grade in grades:
        subsection = CourseSubsections.query.filter_by(course_subsection_id=grade.course_subsection_id).first()
        if subsection:
            # Extract the integer part of the course_subsection_number
            course_section_number = int(float(subsection.course_subsection_number))
            # Query the Courses table to get the course_name
            course = Courses.query.filter(
                Courses.section_number == course_section_number
            ).first()
            
            if course:
                grades_with_names.append({
                    'course_subsection_name': subsection.course_subsection_name,
                    'highest_grade': grade.highest_grade,
                    'course_module_name': course.course_name
                })

    # Get basic dashboard metrics
    total_points = UserPoints.query.filter_by(user_id=user_id).with_entities(UserPoints.num_points).scalar() or 0
    completed_count = StudentAssignedCourses.query.filter_by(user_id=user_id, completion_status=True).count()
    total_hints = 0

    logs_with_hints = UserCodeLogs.query\
        .filter(UserCodeLogs.user_id == user_id)\
        .filter(UserCodeLogs.hints.isnot(None))\
        .filter(UserCodeLogs.hints.notin_(["None", "null", "[]", ""]))\
        .all()
    
    for log in logs_with_hints:
        if isinstance(log.hints, list):
            total_hints += 1
        else:
            try:
                hints_list = json.loads(log.hints)
                total_hints += 1 if hints_list else 0
            except json.JSONDecodeError:
                total_hints += 1 if log.hints else 0

    # Define common page contexts
    page_contexts = [
        "Fetch Reach",
        "Pick and Place",
        "Fetch Stack",
        "Fetch Organize",
        "Fetch Sensors",
        "Car"
    ]
    
    # Calculate attempts data
    attempts_data = {}
    for context in page_contexts:
        total_attempts = db.session.query(func.count(UserCodeLogs.user_log_id)).filter(
            UserCodeLogs.page_context == context,
            UserCodeLogs.user_id == user_id 
        ).scalar() or 0

        completion_count = db.session.query(
            func.count(UserCodeLogs.user_log_id)).filter(
                UserCodeLogs.page_context == context,
                UserCodeLogs.error.is_(None),
                UserCodeLogs.hints.is_(None),
                UserCodeLogs.static_issues.is_(None),
                UserCodeLogs.user_id == user_id
        ).scalar() or 0

        average_attempts = total_attempts / completion_count if completion_count > 0 else 0

        attempts_data[context] = {
            'total_attempts': total_attempts,
            'completion_count': completion_count,
            'average_attempts': average_attempts
        }

    # Generate attempts graph
    contexts = list(attempts_data.keys())
    average_attempts = [attempts_data[context]['average_attempts'] for context in contexts]

    plt.figure(figsize=(10, 5), facecolor='#f8f9fa')
    plt.subplots_adjust(bottom=0.3)
    
    max_attempts = max(average_attempts) if average_attempts else 0
    y_max = max(10, max_attempts * 1.2)  # At least 10, or 20% above max value

    bars = plt.bar(contexts, average_attempts, zorder=3)
    plt.title('Your Average Attempts per Robotic Environment')
    plt.xlabel('Robotic Environment')
    plt.ylabel('Average Number of Attempts Taken')
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, y_max)

    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom')

    plt.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)

    # Save attempts graph to buffer
    buf_attempts = io.BytesIO()
    plt.savefig(buf_attempts, format='png', dpi=100, bbox_inches='tight')
    buf_attempts.seek(0)
    plt.close()

    # Calculate duration data
    duration_data = {}
    for context in page_contexts:
        time_logs = db.session.query(UserTimeLogs).filter(
            UserTimeLogs.page_context == context,
            UserTimeLogs.user_id == user_id,
            UserTimeLogs.duration.isnot(None)
        ).all()
        
        total_duration = sum(log.duration for log in time_logs) if time_logs else 0
        average_duration = total_duration / len(time_logs) if time_logs else 0
        
        duration_data[context] = {
            'total_duration': total_duration,
            'average_duration': average_duration,
            'attempt_count': len(time_logs)
        }

    # Generate duration graph
    contexts_duration = list(duration_data.keys())
    average_durations = [duration_data[context]['average_duration'] for context in contexts_duration]

    plt.figure(figsize=(10, 5), facecolor='#f8f9fa')
    plt.subplots_adjust(bottom=0.3)

    max_duration = max(average_durations) if average_durations else 0
    y_max_duration = max(10, max_duration * 1.2)  # At least 10, or 20% above max value

    bars_duration = plt.bar(contexts_duration, average_durations, color='#2ca02c', zorder=3)
    plt.title('Your Average Time Spent per Robotic Environment')
    plt.xlabel('Robotic Environment')
    plt.ylabel('Average Time Spent (s)')
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, y_max_duration)

    # Add value labels on top of each bar
    for bar in bars_duration:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom')

    plt.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)

    # Save duration graph to buffer
    buf_duration = io.BytesIO()
    plt.savefig(buf_duration, format='png', dpi=100, bbox_inches='tight')
    buf_duration.seek(0)
    plt.close()

    # Prepare dashboard data
    dashboard_data = {
        'points': total_points,
        'completed_courses': completed_count,
        'hints': total_hints,
        'attempts_graph': base64.b64encode(buf_attempts.read()).decode('utf-8'),
        'duration_graph': base64.b64encode(buf_duration.read()).decode('utf-8')
    }

    return render_template(
        'dashboard/student/dashboard_student_grades.html',
        is_dashboard=True,
        is_student_dashboard=True,
        user=user,
        in_class=in_class,
        assignments=assignments,
        grades_with_names=grades_with_names,
        dashboard_data=dashboard_data
    )

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
        return redirect(url_for('RedirectUser'))
    
    user_classes = get_classes(user_id)
    class_count = len(user_classes)
    student_ids = []
    for classes in user_classes:
        enrollments = db.session.query(Enrollment.user_id).filter_by(class_id=classes.class_id).all()
        for enrollment in enrollments:
            student_ids.append(enrollment.user_id)
    unique_student_ids = list(set(student_ids))

    if unique_student_ids:
        subquery = db.session.query(
            StudentGrades.student_id,
            StudentGrades.course_subsection_id,
            func.max(StudentGrades.percentage_grade).label('max_grade')
        ).filter(
            StudentGrades.student_id.in_(unique_student_ids)
        ).group_by(
            StudentGrades.student_id,
            StudentGrades.course_subsection_id
        ).subquery()

        overall_avg_grade = db.session.query(
            func.avg(subquery.c.max_grade)
        ).scalar() or 0.0

    else:
        overall_avg_grade = 0.0

    class_stats = {
        "class_count": class_count,
        "unique_student_count": len(unique_student_ids),
        "overall_avg_grade": round(overall_avg_grade, 2) if overall_avg_grade else 0.0,
    }

    page_contexts = [
    "Fetch Reach",
    "Pick and Place",
    "Fetch Stack",
    "Fetch Organize",
    "Fetch Sensors",
    "Car"
    ]

    results = {}
    for context in page_contexts:
        total_attempts = db.session.query(func.count(UserCodeLogs.user_log_id)).filter(
            UserCodeLogs.page_context == context,
            UserCodeLogs.user_id.in_(unique_student_ids)
        ).scalar() or 0

        completion_count = db.session.query(
        func.count(UserCodeLogs.user_log_id)).filter(
            UserCodeLogs.page_context == context,
            UserCodeLogs.error.is_(None),
            UserCodeLogs.hints.is_(None),
            UserCodeLogs.static_issues.is_(None),
            UserCodeLogs.user_id.in_(unique_student_ids)
        ).scalar() or 0

        

        average_attempts = total_attempts / completion_count if completion_count > 0 else 0

        results[context] = {
        'total_attempts': total_attempts,
        'completion_count': completion_count,
        'average_attempts': average_attempts
        }

        contexts = list(results.keys())
        average_attempts = [results[context]['average_attempts'] for context in contexts]

        plt.figure(figsize=(10, 5), facecolor='#f8f9fa')
        plt.subplots_adjust(bottom=0.3)

        # Set y-axis limits (minimum 0, maximum at least 10 or 20% above max value)
        max_attempts = max(average_attempts) if average_attempts else 0
        y_max = max(10, max_attempts * 1.2)  # At least 10, or 20% above max value

        bars = plt.bar(contexts, average_attempts, zorder=3)
        plt.title('Average Attempts per Robotic Environment')
        plt.xlabel('Robotic Environment')
        plt.ylabel('Average Number of Attempts Taken')
        plt.xticks(rotation=45, ha='right')

        # Set axis limits
        plt.ylim(0, y_max)

        # Add value labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}',
                    ha='center', va='bottom')

        # Add grid lines for better readability
        plt.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)

        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        plt.close()

        graph_image = base64.b64encode(buf.read()).decode('utf-8')


    return render_template('dashboard/instructor/dashboard_instructor.html', 
                           is_dashboard=True, 
                           is_instructor_dashboard=True, 
                           classes=user_classes, 
                           user=user,
                           class_stats=class_stats,
                           graph_image=graph_image)

@app.route('/dashboard/instructor-view/classes', methods=['GET', 'POST'])
def RenderInstructorClasses():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))

    user_id = user['user_id']
    role = user['role_id']
    
    if role != ROLE_INSTRUCTOR:
        flash('You must be an instructor to access this page.', 'popup')
        return redirect(url_for('RedirectUser'))
    
    user_classes = get_classes(user_id)
    courses = Courses.query.order_by(Courses.course_id).all()

    if request.method == 'POST':
        class_course_code = request.form['classCourseCode']
        class_section = request.form['classSection'] 
        class_date = request.form['classDate']

        course_code_valid = is_valid_course_code(class_course_code)
        section_valid = class_section.isdigit() 

        if not course_code_valid:
            flash("Course Code Must Follow the Format: Letters + Numbers.", "popup")

        if not section_valid:
            flash("Section Number Must Not Contain Any Characters.", "popup")

        if not (course_code_valid and section_valid):
            return redirect(url_for('RenderInstructorDashboard'))

        class_section = int(class_section)

        for user_class in user_classes:
            if (class_course_code == user_class.class_course_code and 
                class_section == user_class.class_section_number):
                flash('A class of the same name and section has already been created', 'popup')
                return redirect(url_for('RenderInstructorClasses'))
            
        new_class = Classes()
        new_class.class_course_code = class_course_code
        new_class.class_section_number = class_section
        new_class.expired_at = class_date
        new_class.user_id = user_id
        db.session.add(new_class)
        db.session.commit()
        
        flash('Class created successfully!', 'popup')
        return redirect(url_for('RenderInstructorClasses'))

    class_code = session.get('class_code')
    
    session.pop('class_code', None)

    return render_template('dashboard/instructor/dashboard_classes.html', 
                           is_dashboard=True, 
                           is_instructor_dashboard=True, 
                           classes=user_classes, 
                           class_code=class_code, 
                           user=user, 
                           courses=courses)

@app.route('/dashboard/instructor-view/classes/generate-class-code', methods=['POST'])
def GenerateClassCode():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))

    user_id = user['user_id']
    role = user['role_id']
    
    if role != ROLE_INSTRUCTOR:
        flash('You must be an instructor to access this page.', 'popup')
        return redirect(url_for('RedirectUser'))
    
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
    
@app.route('/dashboard/instructor-view/gradebook')
def RenderInstructorGradebook():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))

    user_id = user['user_id']
    role = user['role_id']
    
    if role != ROLE_INSTRUCTOR:
        flash('You must be an instructor to access this page.', 'popup')
        return redirect(url_for('RedirectUser'))
    
    classes = get_classes(user_id)
    selected_class_id = request.args.get('class_id')
    
    # Get students for selected class
    students = []
    if selected_class_id:
        students = db.session.query(
            User.user_id,
            User.first_name,
            User.last_name,
            Enrollment.enrollment_date,
            StudentGrades.percentage_grade
        ).join(
            Enrollment, User.user_id == Enrollment.user_id
        ).outerjoin(
            StudentGrades, (StudentGrades.student_id == User.user_id) & 
                          (StudentGrades.class_id == Enrollment.class_id)
        ).filter(
            Enrollment.class_id == selected_class_id
        ).all()
    
    return render_template('dashboard/instructor/dashboard_gradebook.html', 
                         is_dashboard=True, 
                         is_instructor_dashboard=True, 
                         user=user,
                         classes=classes,
                         students=students,
                         selected_class_id=selected_class_id)

@app.route('/api/class/<int:class_id>/students')
def get_class_students(class_id):
    if not session.get('user') or session['user']['role_id'] != ROLE_INSTRUCTOR:
        return jsonify({'error': 'Unauthorized'}), 401

    # First get the highest grade per student per subsection
    highest_grades_subq = db.session.query(
        StudentGrades.student_id,
        StudentGrades.course_subsection_id,
        func.max(StudentGrades.percentage_grade).label('max_grade')
    ).join(
        Enrollment, StudentGrades.student_id == Enrollment.user_id
    ).filter(
        Enrollment.class_id == class_id
    ).group_by(
        StudentGrades.student_id,
        StudentGrades.course_subsection_id
    ).subquery()

    # Then calculate the average of these highest grades per student
    students = db.session.query(
        User.user_id,
        User.first_name,
        User.last_name,
        func.coalesce(func.avg(highest_grades_subq.c.max_grade), 0).label('avg_grade')
    ).join(
        Enrollment, User.user_id == Enrollment.user_id
    ).outerjoin(
        highest_grades_subq, highest_grades_subq.c.student_id == User.user_id
    ).filter(
        Enrollment.class_id == class_id
    ).group_by(
        User.user_id,
        User.first_name,
        User.last_name
    ).all()

    return jsonify({
        'students': [{
            'user_id': s.user_id,
            'first_name': s.first_name,
            'last_name': s.last_name,
            'grade': f"{s.avg_grade:.1f}%" if s.avg_grade else "N/A"
        } for s in students]
    })

@app.route('/api/leaderboard')
def get_leaderboard():
    class_id = request.args.get('class_id')
    
    # Get all enrollments for this class
    enrollments = Enrollment.query.filter_by(class_id=class_id).all()
    
    leaderboard = []
    for enrollment in enrollments:
        # Get user points (assuming you have a UserPoints model)
        total_points = db.session.query(
            func.sum(UserPoints.num_points)
        ).filter_by(user_id=enrollment.user_id).scalar() or 0
        
        # Get user details
        user = User.query.get(enrollment.user_id)
        
        leaderboard.append({
            'user_id': user.user_id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'total_points': total_points
        })
    
    # Sort by points (descending)
    leaderboard.sort(key=lambda x: x['total_points'], reverse=True)
    
    return jsonify({
        'leaderboard': leaderboard
    })

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
    is_student = role == ROLE_STUDENT

    if is_student:
        assigned_courses = StudentAssignedCourses.query.filter_by(user_id=user_id)\
        .order_by(StudentAssignedCourses.course_id)\
        .all()
        courses = []
        for assignment in assigned_courses:
            courses.append(assignment.course)

        assigned_subsections = StudentAssignedCourseSubsections.query.filter_by(user_id=user_id).all()
        completed_subsections = StudentAssignedCourseSubsections.query.filter_by(completion_status = 't', user_id=user_id).all()

        num_completed_subsections = len(completed_subsections)
        num_assigned_subsections = len(assigned_subsections)

        if num_assigned_subsections > 0:
            complete_percentage = round((num_completed_subsections / num_assigned_subsections) * 100)
        else:
            complete_percentage = 0
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

    if is_student:
        return(redirect(url_for('RenderStudentRoadmap')))

    return render_template("courses.html", courses=filtered_course_catalog, query=query, user=user, complete_percentage=complete_percentage, is_student=is_student, is_course_page=True)

@app.route('/playground')
def RenderPlayground():
    return render_template('playground.html', is_course_page=True)

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
    return render_template('courses/course1-content/overview.html', module_completed=module_completed, is_course_page=True)

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
    return render_template('courses/course1-content/history_of_robotics.html', module_completed=module_completed, is_course_page=True)

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
    return render_template('courses/course1-content/types_of_robots.html', module_completed=module_completed, is_course_page=True)

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
    return render_template('courses/course1-content/importance_and_app.html', module_completed=module_completed, is_course_page=True)

@app.route('/module1/introduction/course1-quiz-1')
def course1quiz1():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))

    user_id = user['user_id']
    role = user['role_id']
    subsection_number = 1.9
    passing_score = 70.0

    subsection = CourseSubsections.query.filter_by(course_subsection_number=subsection_number).first()

    highest_score = (
        db.session.query(db.func.max(StudentGrades.percentage_grade))
        .filter_by(student_id=user_id, course_subsection_id=subsection.course_subsection_id)
        .scalar()
    )

    if highest_score is None:
        highest_score = 0.0 

    if role == ROLE_STUDENT:
        if highest_score >= passing_score:
            module_completed = update_and_get_module_completion(user_id, subsection_number)
        else:
            module_completed = {}
            subsections = StudentAssignedCourseSubsections.query.filter_by(user_id=user_id).all()

            for subsection in subsections:
                module_completed[subsection.course_subsection_number] = subsection.completion_status
    else:
        module_completed = {}

    return render_template(
        'courses/course1-content/course1-quiz1.html',
        module_completed=module_completed,
        is_course_page=True
    )

@app.route('/get-scores', methods=['GET'])
def get_scores():
    user = session.get('user')
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    user_id = user['user_id']
    subsection_number = request.args.get('subsection_number', type=float)
    if not subsection_number:
        return jsonify({'error': 'subsection_number is required'}), 400

    subsection = CourseSubsections.query.filter_by(course_subsection_number=subsection_number).first()
    if not subsection:
        return jsonify({'error': 'Subsection not found'}), 404
    
    recent_score = (
        db.session.query(StudentGrades.percentage_grade)
        .filter_by(student_id=user_id, course_subsection_id=subsection.course_subsection_id)
        .order_by(StudentGrades.created_at.desc())
        .first()
    )

    highest_score = (
        db.session.query(db.func.max(StudentGrades.percentage_grade))
        .filter_by(student_id=user_id, course_subsection_id=subsection.course_subsection_id)
        .scalar()
    )

    passing_score = 70.0

    recent_score_value = recent_score[0] if recent_score else None

    return jsonify({
        'recent_score': recent_score_value,
        'highest_score': highest_score,
        'passing_score': passing_score
    })

@app.route('/submit-quiz', methods=['POST'])
def submit_quiz():
    user = session.get('user')  # Ensure the user is logged in
    if not user:
        return jsonify({"error": "Unauthorized"}), 403

    role = user['role_id']

    data = request.json
    student_id = user['user_id']
    score = data.get('score', 0)
    print(score)
    total_questions = 10
    percentage_grade = round((score / total_questions) * 100, 2)  # Convert score to percentage
    subsection_number = data.get('subsection_number')

    subsection = CourseSubsections.query.filter_by(course_subsection_number=subsection_number).first()
    if not subsection:
        return jsonify({"error": "Subsection not found"}), 404

    # Save quiz result in database
    new_grade = StudentGrades(
        student_id=student_id,
        percentage_grade=percentage_grade,
        course_subsection_id=subsection.course_subsection_id,
        created_at=datetime.utcnow()
    )

    db.session.add(new_grade)
    db.session.commit()

    most_recent_score = db.session.query(StudentGrades.percentage_grade) \
        .filter_by(student_id=student_id, course_subsection_id=subsection.course_subsection_id) \
        .order_by(StudentGrades.created_at.desc()) \
        .first()

    highest_score = db.session.query(db.func.max(StudentGrades.percentage_grade)) \
        .filter_by(student_id=student_id, course_subsection_id=subsection.course_subsection_id) \
        .scalar()

    passing_score = 70.0

    if role == ROLE_STUDENT:
        if highest_score >= passing_score:
            update_and_get_module_completion(student_id, subsection_number)

    return jsonify({
        "message": "Quiz results saved successfully!",
        "most_recent_score": most_recent_score[0] if most_recent_score else None,
        "highest_score": highest_score if highest_score is not None else 0,
        "passing_score": passing_score
    })

COURSE_PREREQUISITES = {
    22: [21],    # Course 2 requires Course 1
    23: [22],    # Course 3 requires Course 2
    24: [23],    # Course 4 requires Course 3
    25: [],
    26: [],
    27: [],
    28: [],
    29: [],
    30: [],
    31: [],
    32: [],
    33: [],
    34: [],
    35: [],
    36: [],
    37: [],
}

@app.route('/dashboard/student-view/roadmap')
def RenderStudentRoadmap():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))

    user_id = user['user_id']
    role = user['role_id']
    
    if (role != ROLE_STUDENT):
        flash('You must be an student to access this page.', 'popup')
        return redirect(url_for('RedirectUser'))

    # Get only courses assigned to this student, ordered by section number
    student_courses = (
        db.session.query(Courses, StudentAssignedCourses)
        .join(StudentAssignedCourses, Courses.course_id == StudentAssignedCourses.course_id)
        .filter(StudentAssignedCourses.user_id == user_id)
        .order_by(Courses.section_number)
        .all()
    )

    # If no courses are assigned, return empty roadmap
    if not student_courses:
        return render_template(
            'dashboard/student/dashboard_roadmap.html',
            roadmap=[],
            user=user,
            complete_percentage=0,
            courses=[]
        )

    # Create lookup of completed courses - now using completion_status
    completed_courses = {
        sc.course_id: sc.completion_status 
        for c, sc in student_courses 
        if sc.completion_status
    }

    if len(student_courses) > 0:
        progress_percentage = int((len(completed_courses) / len(student_courses)) * 100)
    else:
        progress_percentage = 0

    roadmap = []
    for course, student_course in student_courses:
        # Determine status - now using completion_status
        status = "completed" if student_course.completion_status else "in-progress"
        
        # Check prerequisites - only consider assigned courses
        prereq_met = True
        if course.course_id in COURSE_PREREQUISITES:
            prereq_met = all(
                completed_courses.get(prereq_id, False)
                for prereq_id in COURSE_PREREQUISITES[course.course_id]
            )
        elif course.section_number > 1:  # Linear fallback
            prev_course = next(
                (c for c, sc in student_courses if c.section_number == course.section_number - 1),
                None
            )
            if prev_course:
                prereq_met = completed_courses.get(prev_course.course_id, False)

        # First course should always be unlocked
        unlocked = (course.section_number == 1) or prereq_met
        
        roadmap.append({
            'course_id': course.course_id,
            'course_name': course.course_name,
            'section_number': course.section_number,
            'status': status,
            'prereq_met': prereq_met,
            'locked': not unlocked,
            'certificate': course.certificate,
            'course_desc': course.course_desc,
            'level': course.level,
            'length': course.length,
            'complete_endpoint': url_for('CompleteCourse')  # Add this for form action
        })
    
    return render_template(
        'dashboard/student/dashboard_roadmap.html',
        roadmap=roadmap,
        user=user,
        progress_percentage=progress_percentage,
        complete_percentage=_calculate_completion_percentage(user_id),
        courses=[c for c, sc in student_courses]
    )

def _calculate_completion_percentage(user_id):
    """Calculate completion based on courses (not subsections)"""
    total_courses = StudentAssignedCourses.query.filter_by(user_id=user_id).count()
    completed_courses = StudentAssignedCourses.query.filter_by(
        user_id=user_id,
        completion_status=True  # Changed from is_completed
    ).count()
    return round((completed_courses / total_courses) * 100) if total_courses > 0 else 0

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
    return render_template('courses/course1-content/robot_anatomy.html', module_completed=module_completed, is_course_page=True)

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
    return render_template('courses/course1-content/challenges_in_robotics.html', module_completed=module_completed, is_course_page=True)

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
    return render_template('courses/course1-content/robot_programming.html', module_completed=module_completed, is_course_page=True)

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
    return render_template('courses/course1-content/social_and_ethical_imp.html', module_completed=module_completed, is_course_page=True)

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
    return render_template('courses/course1-content/future_trends.html', module_completed=module_completed, is_course_page=True)

@app.route('/module1/start-page')
def course1_card():
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

    return render_template('courses/course1-content/module_one.html', module_completed=module_completed, is_course_page=True)

@app.route('/module2/start-page-2')
def course2_card():
    return render_template('courses/course2-content/module_two.html', is_course_page=True) 

@app.route('/module3/start-page-3')
def course3_card():
    return render_template('courses/course3-content/module_three.html', is_course_page=True) 

@app.route('/module4/start-page-4')
def course4_card():
    return render_template('courses/course4-content/module_four.html', is_course_page=True) 

@app.route('/module6/start-page-6')
def course6_card():
    return render_template('courses/course6-content/module_six.html', is_course_page=True) 

@app.route('/module7/start-page-7')
def course7_card():
    return render_template('courses/course7-content/module_seven.html', is_course_page=True) 

@app.route('/module8/start-page-8')
def course8_card():
    return render_template('courses/course8-content/module_eight.html', is_course_page=True) 

@app.route('/module9/start-page-9')
def course9_card():
    return render_template('courses/course9-content/module_nine.html', is_course_page=True) 

@app.route('/module10/start-page-10')
def course10_card():
    return render_template('courses/course10-content/module_ten.html', is_course_page=True) 

@app.route('/module11/start-page-11')
def course11_card():
    return render_template('courses/course11-content/module_eleven.html', is_course_page=True) 

@app.route('/module2/introduction')
def module_two():
    return render_template('courses/course2-content/module_two.html', is_course_page=True) 

@app.route('/module2/introduction/introduction-of-mobile-robots')
def intro_of_mobile_robots():
    return render_template('courses/course2-content/intro_of_mobile_robots.html', is_course_page=True)

@app.route('/module2/introduction/idustrial-robots')
def industrial_robots():
    return render_template('courses/course2-content/industrial_robots.html', is_course_page=True)

@app.route('/module2/introduction/service-robots')
def service_robots():
    return render_template('courses/course2-content/service_robots.html', is_course_page=True)

@app.route('/module2/introduction/mobile-robots')
def mobile_robots():
    return render_template('courses/course2-content/mobile_robots.html', is_course_page=True)

@app.route('/module2/introduction/humanoid-robots')
def humanoid_robots():
    return render_template('courses/course2-content/humanoid_robots.html', is_course_page=True)

@app.route('/module2/introduction/agricultural-robots')
def agricultural_robots():
    return render_template('courses/course2-content/agricultural_robots.html', is_course_page=True)

@app.route('/module2/introduction/medical-robots')
def medical_robots():
    return render_template('courses/course2-content/medical_robots.html', is_course_page=True)

@app.route('/module3/introduction')
def module_three():
    return render_template('courses/course3-content/module_three.html', is_course_page=True) 

@app.route('/module3/fetch-reach')
def module_three_fetch_reach():
    return render_template('courses/course3-content/module_three_fetch_reach.html', is_course_page=True) 

@app.route('/module3/autonomous-car')
def module_three_car():
    return render_template('courses/course3-content/module_three_car.html', is_course_page=True) 

@app.route('/module3/fetch-pick-and-place')
def module_three_fetch_pick():
    return render_template('courses/course3-content/module_three_fetch_pick.html', is_course_page=True) 

@app.route('/module3/fetch-sensor')
def module_three_fetch_sensor():
    return render_template('courses/course3-content/module_three_fetch_sensor.html', is_course_page=True) 

@app.route('/module4/introduction')
def module_four():
    return render_template('courses/course4-content/module_four.html', is_course_page=True) 

@app.route('/module4/formatting/naming-conventions')
def module_four_naming_conventions():
    return render_template('courses/course4-content/module_four_naming_conventions.html', is_course_page=True) 

@app.route('/module4/formatting/comments')
def module_four_comments():
    return render_template('courses/course4-content/module_four_comments.html', is_course_page=True) 

@app.route('/module4/formatting/indentation')
def module_four_indentation():
    return render_template('courses/course4-content/module_four_indentation.html', is_course_page=True) 

@app.route('/module4/variables/variables')
def module_four_variables():
    return render_template('courses/course4-content/module_four_variables.html', is_course_page=True) 

@app.route('/module4/controlflow/controlflow')
def module_four_control_flow():
    return render_template('courses/course4-content/module_four_control_flow.html', is_course_page=True) 

@app.route('/module4/controlflow/loops')
def module_four_loops():
    return render_template('courses/course4-content/module_four_loops.html', is_course_page=True) 

@app.route('/module4/controlflow/functions')
def module_four_functions():
    return render_template('courses/course4-content/module_four_functions.html', is_course_page=True) 

@app.route('/module4/debugging/debugging')
def module_four_debugging():
    return render_template('courses/course4-content/module_four_debugging.html', is_course_page=True) 

DOWNLOAD_FOLDER = os.path.join(app.root_path, 'static', 'downloads')
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/module3/cheat-sheet/download')
def module_three_download():
    return render_template('courses/course3-content/module_three_download.html', is_course_page=True)

@app.route('/module4/cheat-sheet/download')
def module_four_download():
    return render_template('courses/course4-content/module_four_download.html', is_course_page=True)

@app.route('/module6/cheat-sheet/download')
def module_six_download():
    return render_template('courses/course6-content/module_six_download.html', is_course_page=True)

@app.route('/module7/cheat-sheet/download')
def module_seven_download():
    return render_template('courses/course7-content/module_seven_download.html', is_course_page=True)

@app.route('/module8/cheat-sheet/download')
def module_eight_download():
    return render_template('courses/course8-content/module_eight_download.html', is_course_page=True)

@app.route('/module9/cheat-sheet/download')
def module_nine_download():
    return render_template('courses/course9-content/module_nine_download.html', is_course_page=True)

@app.route('/module10/cheat-sheet/download')
def module_ten_download():
    return render_template('courses/course10-content/module_ten_download.html', is_course_page=True)

@app.route('/module11/cheat-sheet/download')
def module_eleven_download():
    return render_template('courses/course11-content/module_eleven_download.html', is_course_page=True)

@app.route('/module6/introduction')
def module_six():
    return render_template('courses/course6-content/module_six.html', is_course_page=True)

@app.route('/module6/about-the-fetch-reach-robot')
def module_six_about_the_fetch_reach_robot():
    return render_template('courses/course6-content/module_six_about_the_fetch_reach_robot.html', is_course_page=True)

@app.route('/module6/given')
def module_six_given():
    return render_template('courses/course6-content/module_six_given.html', is_course_page=True)

@app.route('/module6/implementing-logic')
def module_six_code():
    return render_template('courses/course6-content/module_six_code.html', is_course_page=True)

@app.route('/module6/link-to-environment')
def module_six_link():
    return render_template('courses/course6-content/module_six_link.html', is_course_page=True)

@app.route('/module7/introduction')
def module_seven():
    return render_template('courses/course7-content/module_seven.html', is_course_page=True)

@app.route('/module7/about-the-fetch-pick-and-place-robot')
def module_seven_about_the_fetch_pick_and_place_robot():
    return render_template('courses/course7-content/module_seven_about_the_fetch_pick_and_place_robot.html', is_course_page=True)

@app.route('/module7/given')
def module_seven_given():
    return render_template('courses/course7-content/module_seven_given.html', is_course_page=True)

@app.route('/module7/implementing-logic')
def module_seven_code():
    return render_template('courses/course7-content/module_seven_code.html', is_course_page=True)

@app.route('/module7/link-to-environment')
def module_seven_link():
    return render_template('courses/course7-content/module_seven_link.html', is_course_page=True)

@app.route('/module8/introduction')
def module_eight():
    return render_template('courses/course8-content/module_eight.html', is_course_page=True)

@app.route('/module8/about-the-fetch-stack-robot')
def module_eight_about():
    return render_template('courses/course8-content/module_eight_about.html', is_course_page=True)

@app.route('/module8/given')
def module_eight_given():
    return render_template('courses/course8-content/module_eight_given.html', is_course_page=True)

@app.route('/module8/implementing-logic')
def module_eight_code():
    return render_template('courses/course8-content/module_eight_code.html', is_course_page=True)

@app.route('/module8/link-to-environment')
def module_eight_link():
    return render_template('courses/course8-content/module_eight_link.html', is_course_page=True)

@app.route('/module9/introduction')
def module_nine():
    return render_template('courses/course9-content/module_nine.html', is_course_page=True)

@app.route('/module9/about-the-fetch-organize-robot')
def module_nine_about():
    return render_template('courses/course9-content/module_nine_about.html', is_course_page=True)

@app.route('/module9/given')
def module_nine_given():
    return render_template('courses/course9-content/module_nine_given.html', is_course_page=True)

@app.route('/module9/implementing-logic')
def module_nine_code():
    return render_template('courses/course9-content/module_nine_code.html', is_course_page=True)

@app.route('/module9/link-to-environment')
def module_nine_link():
    return render_template('courses/course9-content/module_nine_link.html', is_course_page=True)

@app.route('/module10/introduction')
def module_ten():
    return render_template('courses/course10-content/module_ten.html', is_course_page=True)

@app.route('/module10/about')
def module_ten_about():
    return render_template('courses/course10-content/module_ten_about.html', is_course_page=True)

@app.route('/module10/given')
def module_ten_given():
    return render_template('courses/course10-content/module_ten_given.html', is_course_page=True)

@app.route('/module10/implementing-logic')
def module_ten_code():
    return render_template('courses/course10-content/module_ten_code.html', is_course_page=True)

@app.route('/module10/link-to-environment')
def module_ten_link():
    return render_template('courses/course10-content/module_ten_link.html', is_course_page=True)

@app.route('/module11/introduction')
def module_eleven():
    return render_template('courses/course11-content/module_eleven.html', is_course_page=True)

@app.route('/module11/about')
def module_eleven_about():
    return render_template('courses/course11-content/module_eleven_about.html', is_course_page=True)

@app.route('/module11/given')
def module_eleven_given():
    return render_template('courses/course11-content/module_eleven_given.html', is_course_page=True)

@app.route('/module11/implementing-logic')
def module_eleven_code():
    return render_template('courses/course11-content/module_eleven_code.html', is_course_page=True)

@app.route('/module11/link-to-environment')
def module_eleven_link():
    return render_template('courses/course11-content/module_eleven_link.html', is_course_page=True)

@app.route('/embedded-course-content')
def embedded_course_content():
    return render_template('courses/course10-content/module_ten_given.html', is_course_page=True)  # This page has NO navbar or footer

@app.route('/embedded-course-content-organize')
def embedded_course_content_organize():
     return render_template('courses/course9-content/module_nine_given.html', is_course_page=True)  

@app.route('/embedded-course-content-car')
def embedded_course_content_car():
    return render_template('courses/course11-content/module_eleven_given.html', is_course_page=True)

@app.route('/contact-us', methods=["GET", "POST"])
def RenderContactUs():
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()
        topic = request.form.get("topic", "").strip()

        print(f"Received: {first_name}, {last_name}, {email}, {message}, {topic}")

        if not first_name or not last_name or not email or not message or not topic:
            return jsonify({"status": "error", "message": "All fields, including topic selection, are required!"})

        return jsonify({"status": "success", "message": "Your message has been sent successfully!"})

    return render_template('contact_us.html', is_homepage=True)


@app.route('/about-us')
def RenderAboutUs():
    team_members = [
        {
            "name": "Timothy",
            "role": "Developer",
            "image": "img/timpic.png",
            "linkedin": "https://www.linkedin.com/in/timothy-ang-622258318/",
            "email": "jmmtimang@gmail.com",
            "description": "Timothy is currently a junior at the University of Nevada, Reno, and will quite impressively be graduating early in December 2025 with a degree in Computer Science and Engineering. His course of study is accompanied by three minors in Cybersecurity, Mathematics, and Big Data. Timothy is particularly interested in cybersecurity and the workings of the ever-evolving field. Timothy is consistently honing his hands-on skills in his coursework and extracurricular activities that will prepare him for utmost success in his technology career."
        },
        {
            "name": "Kiana",
            "role": "Developer",
            "image": "img/kianapic.jpg",
            "linkedin": "https://www.linkedin.com/in/kianapartovi/",
            "email": "kianapartovi04@gmail.com",
            "description": "Kiana is an upcoming junior at the University of Nevada, Reno where she actively engages in both her academic along with extracurricular pursuits. She plans to graduate with a degree in Computer Science and Engineering degree along with three minors in: Mathematics, Information Systems, along with Business Administration. She is an active member of the Association for Computing Machinery, Girls Who Code, and TechWise, a Google-sponsored initiative. Kiana is now a three time intern at NASA working in software engineering and data science."
        },
        {
            "name": "Darren",
            "role": "Developer",
            "image": "img/darrenpic.png",
            "linkedin": "https://www.linkedin.com/in/darren-ly-271887300/",
            "email": "darren.ly04@gmail.com",
            "description": "Darren is an upcoming junior at the University of Nevada, Reno. He is on track to graduate early with a degree in Computer Science and Engineering complemented by two minors, being in Mathematics and Cybersecurity. His utmost passion in computer science along with cybersecurity equips him in a continuation of innovatiion. Darren is looking to develop technical and soft skills to prepare himself for a career in the field. In this project, he has explored robotic fundamentals, full stack development, and large language learning models."
        }
    ]
    print("team_members =", team_members)
    return render_template('about_us.html', team_members=team_members, is_homepage=True)

@app.route('/privacy-policy')
def RenderPrivacyPolicy():
    return render_template('privacy-policy.html')

# Darren's Code
@app.route('/Fetch-Reach-Robot')
def RenderFetchReachRobotSimulation():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))
    
    user_id = user['user_id']

    time_log = UserTimeLogs(
        page_context="Fetch Reach",
        start_time=datetime.utcnow(),
        end_time=None,
        duration=None,
        user_id=user_id
    )
    db.session.add(time_log)
    db.session.commit()
    db.session.refresh(time_log)  # This gets the ID for the newly created record

    global env
    close_current_env()
    time.sleep(.1)
    env = ReachEnv()
    return render_template('robotic_environment.html', time_log_id=time_log.time_log_id, is_course_page=True)

@app.route('/update-time-log', methods=['POST'])
def update_time_log():
    data = request.get_json()
    
    if not data or 'time_log_id' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    
    time_log = UserTimeLogs.query.get(data['time_log_id'])
    if not time_log:
        return jsonify({'error': 'Time log not found'}), 404
    
    if 'end_time' in data:
        iso_string = data['end_time'].replace('Z', '+00:00')
        time_log.end_time = datetime.fromisoformat(iso_string)
    if 'duration' in data:
        time_log.duration = data['duration']
    
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/PickAndPlacePage')
def RenderPickAndPlaceEnv():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))
    
    user_id = user['user_id']

    time_log = UserTimeLogs(
        page_context="Fetch Pick and Place",
        start_time=datetime.utcnow(),
        end_time=None,
        duration=None,
        user_id=user_id
    )
    db.session.add(time_log)
    db.session.commit()
    db.session.refresh(time_log)

    global env
    close_current_env()
    time.sleep(.1)
    env = FetchPickAndPlaceEnv()
    return render_template('robotic_pick_and_place_environment.html', time_log_id=time_log.time_log_id, is_course_page=True)

@app.route('/FetchStackPage')
def RenderFetchStackEnv():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))
    
    user_id = user['user_id']

    time_log = UserTimeLogs(
        page_context="Fetch Stack",
        start_time=datetime.utcnow(),
        end_time=None,
        duration=None,
        user_id=user_id
    )
    db.session.add(time_log)
    db.session.commit()
    db.session.refresh(time_log)

    global env
    close_current_env()
    time.sleep(.1)
    env = FetchStackEnv()
    return render_template('fetch_stack_environment.html', time_log_id=time_log.time_log_id, is_course_page=True)

@app.route('/CarPage')
def RenderCarEnv():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))
    
    user_id = user['user_id']

    time_log = UserTimeLogs(
        page_context="Car",
        start_time=datetime.utcnow(),
        end_time=None,
        duration=None,
        user_id=user_id
    )
    db.session.add(time_log)
    db.session.commit()
    db.session.refresh(time_log)
    
    global env
    close_current_env()
    time.sleep(.1)
    env = CarEnv()
    return render_template('robotic_car_environment.html', time_log_id=time_log.time_log_id, is_course_page=True)

@app.route('/FetchOrganizeSensorsPage')
def RenderFetchOrganizeSensorsEnv():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))
    
    user_id = user['user_id']

    time_log = UserTimeLogs(
        page_context="Fetch Sensors",
        start_time=datetime.utcnow(),
        end_time=None,
        duration=None,
        user_id=user_id
    )
    db.session.add(time_log)
    db.session.commit()
    db.session.refresh(time_log)

    global env
    close_current_env()
    time.sleep(.1)
    env = FetchOrganizeSensorsEnv()
    return render_template('robotic_organize_sensors_environment.html', time_log_id=time_log.time_log_id, is_course_page=True)

@app.route('/FetchOrganizePage')
def RenderFetchOrganizeEnv():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))
    
    user_id = user['user_id']

    time_log = UserTimeLogs(
        page_context="Fetch Organize",
        start_time=datetime.utcnow(),
        end_time=None,
        duration=None,
        user_id=user_id
    )
    db.session.add(time_log)
    db.session.commit()
    db.session.refresh(time_log)

    global env
    close_current_env()
    time.sleep(.1)
    env = FetchOrganizeEnv()
    return render_template('robotic_organize_environment.html', time_log_id=time_log.time_log_id, is_course_page=True)

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
                    frame = env.render(mode='rgb_array', width=1440, height=1510)
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
    global env

    # Logging users activity
    user = session.get('user')
    if not user:
        return jsonify({'error': 'You must be logged in to run code.'}), 401

    user_id = user['user_id']

    print("Session user:", user) 
    print("User ID is:", user["user_id"])

    env.reset()

    data = request.get_json(silent=True)

    if data:
        print("Received JSON request.")
        code = data.get('code', '')
        page_context = data.get('context', 'Car') 
    else:
        print("No JSON was received. Using form data in place of the JSON.")
        code = request.form.get('code', '')
        page_context = request.form.get('context', 'Car') 

    if not code:
        return jsonify({'error': 'No code received!', 'static_issues': []}), 400

    user_submitted_code = code
    last_error = None

    print("Final Context Used for Static Analysis:", page_context)
    
    if env is None:
        print("ERROR: No environment initialized before execution!")
        if page_context == "Pick and Place":
            print("Initializing Pick and Place environment inside run-code...")
            env = FetchPickAndPlaceEnv()  

    if env is None: 
            return jsonify({'error': 'No environment chosen yet', 'static_issues': static_issues}), 400
    
    static_issues = analyze_robotics_code(code, context=page_context)
    if page_context == "Pick and Place":
        print("DEBUG")
        print("STATIC ISSUES:", static_issues)
    print("Static Issues Found:", static_issues)

    for issue in static_issues:
        print(f"Found issue at line {issue.get('line', 'Unknown')}: {issue['message']}")

    if static_issues:
        return_data = {
            'message': 'Code contains issues and was not executed.',
            'error': None,
            'static_issues': static_issues,
            'context': page_context,  
        }
        print("Logging the event......")
        print({
            "user_id": user_id,
            "page_context": page_context,
            "code": code,
            "static_issues": static_issues,
            "error": None,
            "hints": []
        })
        print("Current logs for this user:", logs_db.get(user_id, []))

        print("Returning early due to static issues:", return_data)
        return jsonify(return_data)  

    if env is None:
        print("Error: No environment chosen yet")
        return jsonify({'error': 'No environment chosen yet', 'static_issues': static_issues}), 400

    try:
        print("Executing user code...")
        local_context = {}

        code = code.replace("\t", "    ")
        exec(code, globals(), local_context)  

        return_data = {
            'message': 'Code executed successfully.',
            'error': None,
            'static_issues': static_issues,
            'context': page_context,  
        }

        log_event(
            user_id=user_id,
            page_context=page_context,
            code=code,
            static_issues=static_issues,
            error=None,
            hints=[]
        )

        print("Successful Response Data:", return_data)
        return jsonify(return_data)

    except Exception as e:
        last_error = str(e)
        print("Error Message from Run Code:", last_error)
        log_event(
            user_id=user_id,
            page_context=page_context,
            code=code,
            static_issues=static_issues,
            error=last_error,
            hints=[]
        )
        return jsonify({'error': last_error, 'static_issues': static_issues, 'context': page_context})

@app.route('/logs/<int:user_id>', methods=['GET'])
def get_logs(user_id):
    user_logs = logs_db.get(user_id, [])
    print("User logs:", user_logs)  
    return jsonify({"user_id": user_id, "logs": user_logs})

@app.route('/view-logs/<int:user_id>', methods=['GET'])
def view_logs(user_id):
    user_logs = logs_db.get(user_id, [])
    return render_template('display_logs.html', user_id=user_id, logs=user_logs)


# @app.route('/run-code', methods=['POST'])
# def run_code():
#     global user_submitted_code
#     global last_error
#     global static_issues
#     global junk_array

#     env.reset()

#     data = request.get_json(silent=True)

#     if data:
#         print("Received JSON request.")
#         code = data.get('code', '')
#         page_context = data.get('context', 'Car') 
#     else:
#         print("No JSON was received. Using form data in place of the JSON.")
#         code = request.form.get('code', '')
#         page_context = request.form.get('context', 'Car') 

#     if not code:
#         return jsonify({'error': 'No code received!', 'static_issues': []}), 400

#     user_submitted_code = code
#     last_error = None

#     print("Final Context Used for Static Analysis:", page_context)
    
#     static_issues = analyze_robotics_code(code, context=page_context)
#     print("Static Issues Found:", static_issues)

#     for issue in static_issues:
#         print(f"Found issue at line {issue.get('line', 'Unknown')}: {issue['message']}")

#     if env is None:
#         print("Error: No environment chosen yet")
#         return jsonify({'error': 'No environment chosen yet', 'static_issues': static_issues}), 400

#     try:
#         print("Executing user code...")
#         local_context = {}

#         exec(code, globals(), local_context)  

#         # ball_position = local_context.get('ball_position', env.get_ball_position())
#         # gripper_position = local_context.get('gripper_position', env.get_gripper_position())

#         return_data = {
#             'message': 'Code executed successfully.',
#             # 'ball_position': {'x': ball_position[0], 'y': ball_position[1], 'z': ball_position[2]},
#             # 'gripper_position': {'x': gripper_position[0], 'y': gripper_position[1], 'z': gripper_position[2]},
#             'error': None,
#             'static_issues': static_issues,
#             'context': page_context,  
#         }

#         print("Successful Response Data:", return_data)
#         return jsonify(return_data)

#     except Exception as e:
#         last_error = str(e)
#         print("Error Message from Run Code:", last_error)
#         return jsonify({'error': last_error, 'static_issues': static_issues, 'context': page_context})

# @app.route('/get-ball-position', methods=['GET'])
# def get_ball_position():
#     position = env.get_ball_position() 
#     return jsonify({'x': position[0], 'y': position[1], 'z': position[2]})

# @app.route('/get-gripper-position', methods=['GET'])
# def get_gripper_position():
#     position = env.get_gripper_position()  
#     return jsonify({'x': position[0], 'y': position[1], 'z': position[2]})

# @app.route('/get-box-position', methods=['GET'])
# def get_box_position():
#     position = env.get_box_position() 
#     return jsonify({'x': position[0], 'y': position[1], 'z': position[2]})

# @app.route('/check-collision', methods=['GET'])
# def check_collision():
#     ball_position = env.get_ball_position()
#     gripper_position = env.get_gripper_position()
#     # box_position = current_env.get_box_position()
    
    # threshold_distance = 0.01 
    # distance = np.linalg.norm(np.array(ball_position) - np.array(gripper_position))

    # collision_detected = bool(distance < threshold_distance)
    # return jsonify({'collision': collision_detected})

@app.route('/next-question/<quiz_id>', methods=['POST'])
def next_question(quiz_id):
    import importlib

    try:
        quiz_module = importlib.import_module(f'quiz.{quiz_id}')
        quiz = quiz_module.quiz_data
    except ModuleNotFoundError:
        return jsonify({"error": f"No quiz data found for: {quiz_id}"}), 404

    data = request.json

    questions_served = data.get('questions_served', 0)
    score = data.get('score', 0)
    difficulty = data.get('difficulty', 'easy')
    used_questions = data.get('used_questions', [])
    last_correct = data.get('last_correct', True)  # Last answer is correct, move forward

    total_questions = 10

    if questions_served >= 10:
        return jsonify({
            "message": "Quiz complete!",
            "done": True,
            "score": score,
            "total_questions": total_questions
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

    if current_difficulty in quiz["questions"]:
        available_questions = [
            q for q in quiz["questions"][current_difficulty]
            if q not in used_questions
        ]
    
    if not available_questions:
        for next_difficulty in ["easy", "medium", "hard"]:
            if next_difficulty != current_difficulty and next_difficulty in quiz["questions"]:
                available_questions = [
                    q for q in quiz["questions"][next_difficulty]
                    if q not in used_questions
                ]
                if available_questions:
                    current_difficulty = next_difficulty
                    break

    if not available_questions:
        return jsonify({
            "message": "No more questions available!", 
            "done": True, 
            "score": score,
            "total_questions": total_questions
            })

    question = random.choice(available_questions)
    used_questions.append(question)
    questions_served += 1

    return jsonify({
        "question": question,
        "difficulty": current_difficulty,
        "questions_served": questions_served,
        "score": score,
        "used_questions": used_questions,
        "done": False,
        "total_questions": total_questions
    })

# @app.route('/quiz1', methods=['GET'])
# def render_quiz_page():
#     return render_template('quiz1.html')


@app.route('/module1/introduction/course1-quiz-1_2')
def course1quiz1_2():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))

    user_id = user['user_id']
    role = user['role_id']
    subsection_number = 1.91
    passing_score = 70.0

    subsection = CourseSubsections.query.filter_by(course_subsection_number=subsection_number).first()

    highest_score = (
        db.session.query(db.func.max(StudentGrades.percentage_grade))
        .filter_by(student_id=user_id, course_subsection_id=subsection.course_subsection_id)
        .scalar()
    )

    if highest_score is None:
        highest_score = 0.0 

    if role == ROLE_STUDENT:
        if highest_score >= passing_score:
            module_completed = update_and_get_module_completion(user_id, subsection_number)
        else:
            module_completed = {}
            subsections = StudentAssignedCourseSubsections.query.filter_by(user_id=user_id).all()

            for subsection in subsections:
                module_completed[subsection.course_subsection_number] = subsection.completion_status
    else:
        module_completed = {}

    return render_template(
        'courses/course1-content/course1-quiz1_2.html',
        module_completed=module_completed,
        is_course_page=True
    )

@app.route('/module2/types-of-robots/course2-quiz-2')
def course2quiz2():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))

    user_id = user['user_id']
    role = user['role_id']
    subsection_number = 2.9
    passing_score = 70.0

    subsection = CourseSubsections.query.filter_by(course_subsection_number=subsection_number).first()

    highest_score = (
        db.session.query(db.func.max(StudentGrades.percentage_grade))
        .filter_by(student_id=user_id, course_subsection_id=subsection.course_subsection_id)
        .scalar()
    )

    if highest_score is None:
        highest_score = 0.0 

    if role == ROLE_STUDENT:
        if highest_score >= passing_score:
            module_completed = update_and_get_module_completion(user_id, subsection_number)
        else:
            module_completed = {}
            subsections = StudentAssignedCourseSubsections.query.filter_by(user_id=user_id).all()

            for subsection in subsections:
                module_completed[subsection.course_subsection_number] = subsection.completion_status
    else:
        module_completed = {}

    return render_template(
        'courses/course2-content/course2-quiz2.html',
        module_completed=module_completed,
        is_course_page=True
    )

@app.route('/module3/meet-the-robots/course3-quiz-3')
def course3quiz3():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))

    user_id = user['user_id']
    role = user['role_id']
    subsection_number = 3.9
    passing_score = 70.0

    subsection = CourseSubsections.query.filter_by(course_subsection_number=subsection_number).first()

    highest_score = (
        db.session.query(db.func.max(StudentGrades.percentage_grade))
        .filter_by(student_id=user_id, course_subsection_id=subsection.course_subsection_id)
        .scalar()
    )

    if highest_score is None:
        highest_score = 0.0 

    if role == ROLE_STUDENT:
        if highest_score >= passing_score:
            module_completed = update_and_get_module_completion(user_id, subsection_number)
        else:
            module_completed = {}
            subsections = StudentAssignedCourseSubsections.query.filter_by(user_id=user_id).all()

            for subsection in subsections:
                module_completed[subsection.course_subsection_number] = subsection.completion_status
    else:
        module_completed = {}

    return render_template(
        'courses/course3-content/course3-quiz3.html',
        module_completed=module_completed,
        is_course_page=True
    )

@app.route('/module4/coding-practices/course4-quiz-4')
def course4quiz4():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))

    user_id = user['user_id']
    role = user['role_id']
    subsection_number = 4.9
    passing_score = 70.0

    subsection = CourseSubsections.query.filter_by(course_subsection_number=subsection_number).first()

    highest_score = (
        db.session.query(db.func.max(StudentGrades.percentage_grade))
        .filter_by(student_id=user_id, course_subsection_id=subsection.course_subsection_id)
        .scalar()
    )

    if highest_score is None:
        highest_score = 0.0 

    if role == ROLE_STUDENT:
        if highest_score >= passing_score:
            module_completed = update_and_get_module_completion(user_id, subsection_number)
        else:
            module_completed = {}
            subsections = StudentAssignedCourseSubsections.query.filter_by(user_id=user_id).all()

            for subsection in subsections:
                module_completed[subsection.course_subsection_number] = subsection.completion_status
    else:
        module_completed = {}

    return render_template(
        'courses/course4-content/course4-quiz4.html',
        module_completed=module_completed,
        is_course_page=True
    )

@app.route('/module6/fetch-organize/course6-quiz-6')
def course6quiz6():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))

    user_id = user['user_id']
    role = user['role_id']
    subsection_number = 6.9
    passing_score = 70.0

    subsection = CourseSubsections.query.filter_by(course_subsection_number=subsection_number).first()

    highest_score = (
        db.session.query(db.func.max(StudentGrades.percentage_grade))
        .filter_by(student_id=user_id, course_subsection_id=subsection.course_subsection_id)
        .scalar()
    )

    if highest_score is None:
        highest_score = 0.0 

    if role == ROLE_STUDENT:
        if highest_score >= passing_score:
            module_completed = update_and_get_module_completion(user_id, subsection_number)
        else:
            module_completed = {}
            subsections = StudentAssignedCourseSubsections.query.filter_by(user_id=user_id).all()

            for subsection in subsections:
                module_completed[subsection.course_subsection_number] = subsection.completion_status
    else:
        module_completed = {}

    return render_template(
        'courses/course6-content/course6-quiz6.html',
        module_completed=module_completed,
        is_course_page=True
    )

@app.route('/module7/fetch-pick-and-place/course7-quiz-7')
def course7quiz7():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))

    user_id = user['user_id']
    role = user['role_id']
    subsection_number = 7.9
    passing_score = 70.0

    subsection = CourseSubsections.query.filter_by(course_subsection_number=subsection_number).first()

    highest_score = (
        db.session.query(db.func.max(StudentGrades.percentage_grade))
        .filter_by(student_id=user_id, course_subsection_id=subsection.course_subsection_id)
        .scalar()
    )

    if highest_score is None:
        highest_score = 0.0 

    if role == ROLE_STUDENT:
        if highest_score >= passing_score:
            module_completed = update_and_get_module_completion(user_id, subsection_number)
        else:
            module_completed = {}
            subsections = StudentAssignedCourseSubsections.query.filter_by(user_id=user_id).all()

            for subsection in subsections:
                module_completed[subsection.course_subsection_number] = subsection.completion_status
    else:
        module_completed = {}

    return render_template(
        'courses/course7-content/course7-quiz7.html',
        module_completed=module_completed,
        is_course_page=True
    )

@app.route('/module8/fetch-stack/course8-quiz-8')
def course8quiz8():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))

    user_id = user['user_id']
    role = user['role_id']
    subsection_number = 8.9
    passing_score = 70.0

    subsection = CourseSubsections.query.filter_by(course_subsection_number=subsection_number).first()

    highest_score = (
        db.session.query(db.func.max(StudentGrades.percentage_grade))
        .filter_by(student_id=user_id, course_subsection_id=subsection.course_subsection_id)
        .scalar()
    )

    if highest_score is None:
        highest_score = 0.0 

    if role == ROLE_STUDENT:
        if highest_score >= passing_score:
            module_completed = update_and_get_module_completion(user_id, subsection_number)
        else:
            module_completed = {}
            subsections = StudentAssignedCourseSubsections.query.filter_by(user_id=user_id).all()

            for subsection in subsections:
                module_completed[subsection.course_subsection_number] = subsection.completion_status
    else:
        module_completed = {}

    return render_template(
        'courses/course8-content/course8-quiz8.html',
        module_completed=module_completed,
        is_course_page=True
    )

@app.route('/module9/fetch-organize/course9-quiz-9')
def course9quiz9():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))

    user_id = user['user_id']
    role = user['role_id']
    subsection_number = 9.9
    passing_score = 70.0

    subsection = CourseSubsections.query.filter_by(course_subsection_number=subsection_number).first()

    highest_score = (
        db.session.query(db.func.max(StudentGrades.percentage_grade))
        .filter_by(student_id=user_id, course_subsection_id=subsection.course_subsection_id)
        .scalar()
    )

    if highest_score is None:
        highest_score = 0.0 

    if role == ROLE_STUDENT:
        if highest_score >= passing_score:
            module_completed = update_and_get_module_completion(user_id, subsection_number)
        else:
            module_completed = {}
            subsections = StudentAssignedCourseSubsections.query.filter_by(user_id=user_id).all()

            for subsection in subsections:
                module_completed[subsection.course_subsection_number] = subsection.completion_status
    else:
        module_completed = {}

    return render_template(
        'courses/course9-content/course9-quiz9.html',
        module_completed=module_completed,
        is_course_page=True
    )

@app.route('/module10/fetch-sensors/course10-quiz-10')
def course10quiz10():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))

    user_id = user['user_id']
    role = user['role_id']
    subsection_number = 10.9
    passing_score = 70.0

    subsection = CourseSubsections.query.filter_by(course_subsection_number=subsection_number).first()

    highest_score = (
        db.session.query(db.func.max(StudentGrades.percentage_grade))
        .filter_by(student_id=user_id, course_subsection_id=subsection.course_subsection_id)
        .scalar()
    )

    if highest_score is None:
        highest_score = 0.0 

    if role == ROLE_STUDENT:
        if highest_score >= passing_score:
            module_completed = update_and_get_module_completion(user_id, subsection_number)
        else:
            module_completed = {}
            subsections = StudentAssignedCourseSubsections.query.filter_by(user_id=user_id).all()

            for subsection in subsections:
                module_completed[subsection.course_subsection_number] = subsection.completion_status
    else:
        module_completed = {}

    return render_template(
        'courses/course10-content/course10-quiz10.html',
        module_completed=module_completed,
        is_course_page=True
    )

@app.route('/module11/autonomous-car/course11-quiz-11')
def course11quiz11():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))

    user_id = user['user_id']
    role = user['role_id']
    subsection_number = 11.9
    passing_score = 70.0

    subsection = CourseSubsections.query.filter_by(course_subsection_number=subsection_number).first()

    highest_score = (
        db.session.query(db.func.max(StudentGrades.percentage_grade))
        .filter_by(student_id=user_id, course_subsection_id=subsection.course_subsection_id)
        .scalar()
    )

    if highest_score is None:
        highest_score = 0.0 

    if role == ROLE_STUDENT:
        if highest_score >= passing_score:
            module_completed = update_and_get_module_completion(user_id, subsection_number)
        else:
            module_completed = {}
            subsections = StudentAssignedCourseSubsections.query.filter_by(user_id=user_id).all()

            for subsection in subsections:
                module_completed[subsection.course_subsection_number] = subsection.completion_status
    else:
        module_completed = {}

    return render_template(
        'courses/course11-content/course11-quiz11.html',
        module_completed=module_completed,
        is_course_page=True
    )

@app.route("/certificate/module2")
def module_two_certificate():
    return render_template('courses/course2-content/module_two_certificate.html') 

@app.route("/certificate/module3")
def module_three_certificate_meet():
    return render_template('courses/course3-content/module_three_certificate_meet.html') 

@app.route("/certificate/module4")
def module_four_certificate_code():
    return render_template('courses/course4-content/module_four_certificate_code.html') 

@app.route("/certificate/module6")
def module_six_certificate_reach():
    return render_template('courses/course6-content/module_six_certificate_reach.html') 

@app.route("/certificate/module7")
def module_seven_certificate_pick_and_place():
    return render_template('courses/course7-content/module_seven_certificate_pick_and_place.html') 

@app.route("/certificate/module8")
def module_eight_certificate_stack():
    return render_template('courses/course8-content/module_eight_certificate_stack.html') 

@app.route("/certificate/module9")
def module_nine_certificate_organize():
    return render_template('courses/course9-content/module_nine_certificate_organize.html') 

@app.route("/certificate/module10")
def module_ten_certificate_organize_sensors():
    return render_template('courses/course10-content/module_ten_certificate_organize_sensors.html') 

@app.route("/certificate/module11")
def module_eleven_certificate_car():
    return render_template('courses/course11-content/module_eleven_certificate_car.html') 

def generate_certificate():
    """Generates a certificate image with the given text and returns it as a BytesIO object."""
    # Load the certificate template
    image = Image.open("static/certificate_template.png")
    draw = ImageDraw.Draw(image)

    name = "John Doe"
    date = "4/24/2025"
    text_color = (0, 0, 0)
    name_font_size = 100
    date_font_size = 50

    try:
        name_font = ImageFont.truetype("static/cookie-regular.ttf", name_font_size)
    except OSError:
        name_font = ImageFont.load_default()

    image_width, image_height = image.size

    # Calculate text position (centered horizontally, slightly lower vertically)
    name_bbox = name_font.getbbox(name)
    name_text_width = name_bbox[2] - name_bbox[0]  # Width of the text
    name_text_height = name_bbox[3] - name_bbox[1]  # Height of the text

    name_x_offset = 0
    name_y_offset = 75
    name_x = (image_width - name_text_width) // 2 + name_x_offset
    name_y = (image_height - name_text_height) // 2 + name_y_offset

    try:
        date_font = ImageFont.truetype("static/cookie-regular.ttf", date_font_size)
    except OSError:
        date_font = ImageFont.load_default()

    date_bbox = date_font.getbbox(date)
    date_text_width = date_bbox[2] - date_bbox[0]
    date_text_height = date_bbox[3] - date_bbox[1]

    date_x_offset = 155
    date_y_offset = 140
    date_x = 0 + date_x_offset #Increasing x = move rightwards
    date_y = (image_height - date_text_height) - date_y_offset #Increasing y = move downwards

    # Draw the text on the image
    draw.text((name_x, name_y), name, font=name_font, fill=text_color)
    draw.text((date_x, date_y), date, font=date_font, fill=text_color)

    # Convert image to bytes
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    return img_bytes

@app.route("/view_certificate")
def view_certificate():
    """Returns the generated certificate as an image."""
    img_bytes = generate_certificate()
    return Response(img_bytes.getvalue(), mimetype="image/png")

@app.route("/download_certificate")
def download_certificate():
    """Returns the generated certificate as a downloadable PDF."""
    img_bytes = generate_certificate()

    # Convert the image to PDF
    pdf_bytes = io.BytesIO()
    Image.open(img_bytes).save(pdf_bytes, format="PDF")
    pdf_bytes.seek(0)

    return send_file(
        pdf_bytes,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="certificate.pdf"
    )

@app.route("/dashboard", methods=['POST'])
def CompleteCourse():
    course_id = request.form.get('course_id')
    completed = request.form.get('completed') == 'true'

    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.')
        return redirect(url_for('RenderLogin'))

    user_id = user['user_id']
    role = user['role_id']

    if course_id and completed:
        assigned_course = StudentAssignedCourses.query.filter_by(
            course_id=course_id,
            user_id=user_id
        ).first()
        
        if assigned_course:
            if not assigned_course.completion_status:
                assigned_course.completion_status = True
                
                points_record = UserPoints.query.filter_by(user_id=user_id).first()
                if points_record:
                    points_record.num_points += 1000.0
                    flash('1000 points added to your total!', 'popup')
                else:
                    points_record = UserPoints(num_points=1000.0, user_id=user_id)
                    db.session.add(points_record)
                    flash('1000 points awarded!', 'popup')
                
                db.session.commit()
            else:
                flash('Course was already completed - no points awarded.', 'popup')
        else:
            if role == ROLE_STUDENT:
                flash('Course assignment not found.', 'popup')

    if role == ROLE_STUDENT:
        return redirect(url_for('RenderStudentDashboard', course_id=course_id, completed=completed))
    elif role == ROLE_INSTRUCTOR:
        return redirect(url_for('RenderInstructorDashboard'))
    elif role == ROLE_ADMIN:
        return redirect(url_for('RenderAdminDashboard'))
    
    return render_template('account/login.html', is_homepage=True)

@app.route('/dashboard/instructor-view/student-code-log/student-id-<int:student_id>')
def RenderStudentCodeLogs(student_id):
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.', 'popup')
        return redirect(url_for('RenderHomepage'))

    user_id = user['user_id'] 
    role = user['role_id']
    
    if role != ROLE_INSTRUCTOR:
        flash('You must be an instructor to access this page.', 'popup')
        return redirect(url_for('RenderStudentDashboard'))
    
    # Initialize totals
    totals = {
        'submissions': 0,
        'errors': 0,
        'hints': 0,
        'static_issues': 0,
        'successes': 0
    }

    # Query the time logs and calculate durations per page context
    time_logs = db.session.query(
        UserTimeLogs.page_context,
        func.sum(UserTimeLogs.duration).label('total_duration')
    ).filter(
        UserTimeLogs.user_id == student_id,
        UserTimeLogs.duration.isnot(None)  # Only include logs with duration
    ).group_by(
        UserTimeLogs.page_context
    ).all()

    # Convert to dictionary for easy lookup
    page_durations = {log.page_context: log.total_duration for log in time_logs}

    # Query the code logs
    raw_logs = db.session.query(
        UserCodeLogs.user_log_id,
        UserCodeLogs.code,
        UserCodeLogs.error,
        UserCodeLogs.hints,
        UserCodeLogs.page_context,
        UserCodeLogs.static_issues,
        UserCodeLogs.created_at
    ).filter(
        UserCodeLogs.user_id == student_id
    ).order_by(
        UserCodeLogs.created_at.desc()
    ).all()

    # Process logs and calculate totals
    code_logs = []
    for log in raw_logs:
        totals['submissions'] += 1
        
        log_dict = {
            'user_log_id': log.user_log_id,
            'code': log.code,
            'error': log.error,
            'hints': log.hints,
            'page_context': log.page_context,
            'static_issues': log.static_issues,
            'created_at': log.created_at,
            'counts': {
                'errors': 0,
                'hints': 0,
                'static_issues': 0,
                'is_success': False,
                'duration': page_durations.get(log.page_context, 0)  # Add duration for this page context
            }
        }

        # Check if this is a success case
        is_success = True
        
        # Check error
        if log_dict['error'] and log_dict['error'] not in ["None", "null", ""]:
            log_dict['counts']['errors'] = 1
            totals['errors'] += 1
            is_success = False

        # Check hints
        if log_dict['hints'] and log_dict['hints'] not in ["None", "null", "[]", ""]:
            if isinstance(log_dict['hints'], list):
                hint_count = 1  # Treat the entire list as 1 hint
            else:
                try:
                    hints_list = json.loads(log_dict['hints'])
                    hint_count = 1 if hints_list else 0  # Still count as 1 if not empty
                except json.JSONDecodeError:
                    hint_count = 1 if log_dict['hints'] else 0
            
            log_dict['counts']['hints'] = hint_count
            totals['hints'] += hint_count
            is_success = False

        # Check static issues
        if log_dict['static_issues'] and log_dict['static_issues'] not in ["None", "null", "[]", ""]:
            try:
                issues_list = json.loads(log_dict['static_issues'])
                issue_count = len(issues_list) if isinstance(issues_list, list) else 1
                log_dict['counts']['static_issues'] = issue_count
                totals['static_issues'] += issue_count
                is_success = False
            except json.JSONDecodeError:
                if log_dict['static_issues']:
                    log_dict['counts']['static_issues'] = 1
                    totals['static_issues'] += 1
                    is_success = False

        # If all checks passed, count as success
        if is_success:
            totals['successes'] += 1
            log_dict['counts']['is_success'] = True

        code_logs.append(log_dict)

    # Add total time spent to the template context
    totals['total_time'] = sum(page_durations.values()) if page_durations else 0

    # Map page contexts to friendly names
    page_contexts = {
        "/Fetch-Reach-Robot": "Fetch Reach",
        "/PickAndPlacePage": "Fetch Pick and Place",
        "/FetchStackPage": "Fetch Stack",
        "/FetchOrganizePage": "Fetch Organize",
        "/FetchOrganizeSensorsPage": "Fetch Sensors",
        "/CarPage": "Car", 
    }

    return render_template('dashboard/instructor/dashboard_code_logs.html', 
                         code_logs=code_logs,
                         totals=totals,
                         page_contexts=page_contexts,
                         page_durations=page_durations)

@app.route('/dashboard')
def RedirectUser():
    user = session.get('user')
    if not user:
        flash('You must be logged in to access this page.', 'popup')
        return redirect(url_for('RenderHomepage'))

    user_id = user['user_id'] 
    role = user['role_id']
    
    if role == ROLE_INSTRUCTOR:
        return redirect(url_for('RenderInstructorDashboard'))
    if role == ROLE_ADMIN:
        return redirect(url_for('RenderAdminDashboard'))
    if role == ROLE_STUDENT:
        return redirect(url_for('RenderStudentDashboard'))

    return redirect(url_for('RenderHomeage'))




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False, FLASK_DEBUG=0)

