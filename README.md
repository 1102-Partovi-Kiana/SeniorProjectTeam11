# SeniorProjectTeam11

Overview:
The Project: A web-based platform designed to streamline and enhance the learning experience for undergraduate students interested and wanting to get into the fields of robotics. More specifically, we are refactoring a codebase and adding additional features to make it our own with updated libraries. Our project is a National Science Foundation Project.

NSF Team:
Dave Feil-Seifer (PI) Sergiu Dascalu (Co-PI), Frederick C. Harris, Jr. (Co-PI) – all UNR Computer Science and Engineering.
Hossein Jamali (Advisor)

Tech Stack:
Front End:
Flask with Jinja, HTML, JavaScript, CSS
Back End:
Flask and Python
Database:
PostgreSQL
Deployment:
AWS

Code Resources:
Robotics Environment from Mujoco-py Robotics (2.1.2.14)
https://pypi.org/project/mujoco-py/

Car Design From https://github.com/google-deepmind/mujoco/blob/main/model/car/car.xml

Code Contribution
Darren:
I worked on:
app.py (Robotics and Helped with Chatbot Setup)
car.py
organize_sensors.py
organize.py
pickandplace.py
reach.py
stack.py

In SeniorProjectTeam11\flask_app\venv38\lib64\python3.8\site-packages\gym\envs\robotics\assets...
/fetch:
organize_with_sensors.xml
organize.xml
sensor_robot.xml
stack.xml

/car:
car.xml

In SeniorProjectTeam11\flask_app\templates...: (Robotic Environments)
fetch_stack_environment.html
robotic_car_environment.html
robotic_environment.html
robotic_organize_environment.html
robotic_organize_sensors_environment.html
robotic_pick_and_place_environment.html

Kiana:
app.py (Pair Programmed ChatBot SetUp, All other ChatBot Related code, All of the courses logic, 
def run_code() pair programmed with Darren)

base.html

All UI & frontend except for dashboard:

custom.css
other.css

courses/course1-content/challenges_in_robotics.html
courses/course1-content/course1_card.html
courses/course1-content/course1_quiz1.html
courses/course1-content/future_trends.html
courses/course1-content/history_of_robotics.html
courses/course1-content/importance_and_app.html
courses/course1-content/module_intro.html
courses/course1-content/overview.html
courses/course1-content/robot_anatomy.html
courses/course1-content/robot_programming.html
courses/course1-content/social_and_ethical_imp.html
courses/course1-content/types_of_robots.html

courses/course2-content/course2_card.html
courses/course2-content/industrial_robots.html
courses/course2-content/intro_of_mobile_robots.html
courses/course2-content/module_two.html

snippets/navbar.html
snippets/footer.html

courses.html
homepage.html
playgroun.html

Note: Darren has code in these files, and his part is commented in each one
robotic_pick_and_place_environemnt.html
robotic_organize_sensors_environemnt.html
robotic_organize_environemnt.html
robotic_environment.html
robotic_car_environment.html
fetch_stack_enbironment.html
ennvironemnts-landing.html 

Javascript

back-to-top.js
chatbot.js
chatbot2.js
closebot.js
course.js
hamburger.js
home.js
microphone.js
navbar-toggler.js
playground.js
playpausebutton.js
popup-alert.js
signup.js
slider.js
stars.js
tooltip.js

Got all of our vidoes, images, etc.

Timothy:
app.py (Login, Signup, Reset Password, Forgot Password, Student/Instructor Dashboard, Session Logic, etc.)

Note: Paired Programmed with Darren to get the Gymnasium Robot videos to play

CORE_DB.sql
email_func.py
auth_func.py
class_py.py

dashboard/dashboard_classes.html
dashboard/dashboard_instructor.html
dashboard/dashboard_student.html

alert/full.html

account/reset_password.html
account/forgot_password.html
account/forgot_password.txt

snippets/footer.html
snippets/navbar.html

courses/courses3-content/.html (Collabed on it with Darren)

Javascript
sidebar-toggler.js
signup.js
dashboard.js

CSS
dashboard.css
custom.css (editted navbar & footer)
