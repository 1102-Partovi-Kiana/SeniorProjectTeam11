from flask import Flask, render_template, request, jsonify, Response
import mujoco_py
import numpy as np
import cv2  # Import OpenCV
from reach import ReachEnv  # Ensure this imports your ReachEnv class
import requests  # Import requests library for API communication

app = Flask(__name__, static_folder='static')
app.secret_key = "12345999999"

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

attempt_counter = 0
api_key = "AIzaSyDpL6NsK8v8alk8JPVmu9S1QF8oRNhCJDU"  

@app.route('/chatbot-api', methods=['POST'])
def ChatbotAPI():
    print("Chatbot API called")  # Check if the function is called
    global attempt_counter, user_submitted_code
    user_message = request.json.get('message')
    
    print("Received user message:", user_message)  # Verify message received

    if not user_message:
        return jsonify({'error': 'Message is required'}), 400

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
                            "text": user_message
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
    if attempt_counter < 3:
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
