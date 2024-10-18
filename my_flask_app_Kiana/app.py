from flask import Flask, render_template, request, jsonify, Response
import mujoco_py
import numpy as np
import cv2  # Import OpenCV
from reach import ReachEnv  # Ensure this imports your ReachEnv class
import requests  # Import requests library for API communication

app = Flask(__name__, static_folder='static')

env = ReachEnv()  # Initialize your environment here

# Route for the homepage
@app.route('/')
def RenderHomepage():
    return render_template('homepage.html')

@app.route('/robotic-environment')
def RenderRoboticEnvironment():
    return render_template('robotic_environment.html')

@app.route('/Chatbot')
def RenderChatbot():
    return render_template('chatbot.html')

@app.route('/chatbot-api', methods=['POST'])
def ChatbotAPI():
    user_message = request.json.get('message')  # Get user's message from frontend
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400

    try:
        api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
        api_key = "AIzaSyDpL6NsK8v8alk8JPVmu9S1QF8oRNhCJDU"  # Replace with your actual API key

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": user_message
                        }
                    ]
                }
            ]
        }

        response = requests.post(f"{api_url}?key={api_key}", headers={
            'Content-Type': 'application/json'
        }, json=payload)

        # Debugging: Print the full API response
        print("API Response:", response.text)  # Log the full response for inspection

        if response.status_code != 200:
            return jsonify({'error': f'Error from API: {response.text}'}), 500

        response_json = response.json()

        # Updated response parsing
        if 'candidates' in response_json and len(response_json['candidates']) > 0:
            if 'content' in response_json['candidates'][0] and 'parts' in response_json['candidates'][0]['content'] and len(response_json['candidates'][0]['content']['parts']) > 0:
                chatbot_response = response_json['candidates'][0]['content']['parts'][0].get('text', 'No response')
            else:
                chatbot_response = 'No parts available in the response'
        else:
            chatbot_response = 'No contents available in the response'

        return jsonify({'reply': chatbot_response})  # Send response back to the frontend

    except Exception as e:
        return jsonify({'error': str(e)}), 500




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
        first_name = request.form.get('inputFirstName')
        last_name = request.form.get('inputLastName')
        email = request.form.get('inputEmail')
        password = request.form.get('inputPassword')
        # Perform validation and account creation logic here
        return redirect(url_for('RenderHomepage'))

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
        frame = env.render(mode='rgb_array')
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/run-code', methods=['POST'])
def run_code():
    global env  # Access the global environment instance
    code = request.form.get('code')  # Get the code from form data
    print("Executing code:", code)  # Log the code to the console
    try:
        exec(code, {'__builtins__': None, 'env': env})  # Pass the global env
        return jsonify({'message': 'Code executed successfully.'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
