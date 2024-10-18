from flask import Flask, render_template, request, redirect, url_for
from flask import Flask, render_template, Response, request, jsonify
import mujoco_py
import numpy as np
import cv2  # Import OpenCV
from reach import ReachEnv  # Ensure this imports your ReachEnv class


app = Flask(__name__, static_folder='static')

env = ReachEnv()  # Initialize your environment here
# Route for the homepage
@app.route('/')
def RenderHomepage():
    return render_template('homepage.html')

@app.route('/robotic-environment')
def RenderRoboticEnvironment():
    return render_template('robotic_environment.html')

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
    # Example logic to find the environment by id
    environments = [
        {
            'id': 1,
            'name': 'FetchPickAndPlace-v1',
            'brief_description': 'Move the box to the floating goal position.',
            'preview_filename': 'fetchpickandplace.mp4'
        },
        # Add more environments as needed
    ]
    
    # Find the environment with the given ID
    environment = next((env for env in environments if env['id'] == environment_id), None)
    
    if environment is None:
        return "Environment not found", 404

    return render_template('environment_detail.html', environment=environment)

@app.route('/signup', methods=['GET', 'POST'])
def RenderSignup():
    if request.method == 'POST':
        # Handle sign-up logic here, e.g., validate inputs and create the account
        first_name = request.form.get('inputFirstName')
        last_name = request.form.get('inputLastName')
        email = request.form.get('inputEmail')
        password = request.form.get('inputPassword')
        # Perform validation and account creation logic here
        # You would typically save the user information in the database here
        
        return redirect(url_for('RenderHomepage'))  # Redirect after successful sign-up

    # If the request method is GET, return the signup form
    return render_template('account/signup.html')


@app.route('/login')
def RenderLogin():
    if request.method == 'POST':
        first_name = request.form.get('inputFirstName')
        last_name = request.form.get('inputLastName')
        email = request.form.get('inputEmail')
        password = request.form.get('inputPassword')
    return render_template('account/login.html')

@app.route('/courses')
def RenderCourses():
    return render_template('courses.html')

@app.route('/DarrenPage')
def RenderDarrenEnv():
    return render_template('robotic_environment.html')

def generate_frames():
    global env  # Access the global environment instance
    while True:

        # Capture a frame from the MuJoCo viewer
        frame = env.render(mode='rgb_array')

        # Convert frame to a format suitable for streaming
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame as part of the response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/run-code', methods=['POST'])
def run_code():
    global env  # Access the global environment instance
    code = request.form.get('code')  # Get the code from form data
    print("Executing code:", code)  # Log the code to the console
    try:
        # Execute the code with the environment in the global context
        exec(code, {'__builtins__': None, 'env': env})  # Pass the global env
        return jsonify({'message': 'Code executed successfully.'})
    except Exception as e:
        return jsonify({'error': str(e)})

# Debug mode allows for automatic reloading and better error messages
if __name__ == '__main__':
    app.run(debug=True)
