from flask import Flask, render_template, request, jsonify, Response
import mujoco_py
import numpy as np
import cv2 
from reach import ReachEnv  # Ensure this imports your ReachEnv class
from pickandplace import FetchPickAndPlaceEnv
import requests  # Import requests library for API communication

app = Flask(__name__, static_folder='static')

#current_env = FetchPickAndPlaceEnv()
current_env = ReachEnv()

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
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400

    try:
        api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
        api_key = "AIzaSyDpL6NsK8v8alk8JPVmu9S1QF8oRNhCJDU" # Our API Key

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

        if response.status_code != 200:
            return jsonify({'error': f'Error from API: {response.text}'}), 500

        response_json = response.json()

        if 'candidates' in response_json and len(response_json['candidates']) > 0:
            if 'content' in response_json['candidates'][0] and 'parts' in response_json['candidates'][0]['content'] and len(response_json['candidates'][0]['content']['parts']) > 0:
                chatbot_response = response_json['candidates'][0]['content']['parts'][0].get('text', 'No response')
            else:
                chatbot_response = 'No parts available in the response'
        else:
            chatbot_response = 'No contents available in the response'

        return jsonify({'reply': chatbot_response}) 

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Select environment to use (in progress)
@app.route('/select-environment/<env_type>', methods=['GET'])
def select_environment(env_type):
    global current_env
    if env_type == 'reach':
        current_env = ReachEnv()
    elif env_type == 'pickandplace':
        current_env = FetchPickAndPlaceEnv()
    else:
        return jsonify({'error': 'Invalid environment type'}), 400

    return jsonify({'message': f'Selected environment: {env_type}'})

@app.route('/environments')
def RenderEnvironmentList():
    environments = [
        {
            'id': 1,
            'name': 'FetchPickAndPlace-v1',
            'brief_description': 'Move the box to the floating goal position.',
            'preview_filename': 'fetchpickandplace.mp4'
        },
        {
            'id': 2,
            'name': 'Reach-v1',
            'brief_description': 'Reach for the ball and manipulate it.',
            'preview_filename': 'reach.mp4' 
        },
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
        {
            'id': 2,
            'name': 'Reach-v1',
            'brief_description': 'Reach for the ball and manipulate it.',
            'preview_filename': 'reach.mp4' 
        },
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
        return redirect(url_for('RenderHomepage'))

    return render_template('account/signup.html')

@app.route('/login')
def RenderLogin():
    return render_template('account/login.html') 

@app.route('/courses')
def RenderCourses():
    return render_template('courses.html')

@app.route('/ReachPage')
def RenderFetchReachEnv():
    return render_template('robotic_reach_environment.html')

@app.route('/PickAndPlacePage')
def RenderFetchPickAndPlaceEnv():
    return render_template('robotic_pick_and_place_environment.html')

def generate_frames():
    global current_env
    while True:
        if current_env is not None:
            frame = current_env.render(mode='rgb_array')
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
    
    if current_env is None:
        return jsonify({'error': 'No environment selected'}), 400
    
    try:
        local_context = {}
        exec(code, globals(), local_context)

        ball_position = local_context.get('ball_position', current_env.get_ball_position())
        gripper_position = local_context.get('gripper_position', current_env.get_gripper_position())
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
    position = current_env.get_ball_position() 
    return jsonify({'x': position[0], 'y': position[1], 'z': position[2]})

@app.route('/get-gripper-position', methods=['GET'])
def get_gripper_position():
    position = current_env.get_gripper_position()  
    return jsonify({'x': position[0], 'y': position[1], 'z': position[2]})

@app.route('/get-box-position', methods=['GET'])
def get_box_position():
    position = current_env.get_box_position() 
    return jsonify({'x': position[0], 'y': position[1], 'z': position[2]})

@app.route('/check-collision', methods=['GET'])
def check_collision():
    ball_position = current_env.get_ball_position()
    gripper_position = current_env.get_gripper_position()
    # box_position = current_env.get_box_position()
    
    threshold_distance = 0.01 
    distance = np.linalg.norm(np.array(ball_position) - np.array(gripper_position))

    collision_detected = bool(distance < threshold_distance)
    return jsonify({'collision': collision_detected})

if __name__ == '__main__':
    app.run(debug=True)