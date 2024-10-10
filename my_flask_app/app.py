from flask import Flask, render_template, Response, request, jsonify
import mujoco_py
import numpy as np
import cv2  # Import OpenCV
from reach import ReachEnv  # Ensure this imports your ReachEnv class

app = Flask(__name__)

# Global variable to hold the environment instance
env = ReachEnv()  # Initialize your environment here

@app.route('/')
def RenderHomepage():
    return render_template('homepage.html')

@app.route('/robotic-environment')
def RenderRoboticEnvironment():
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

if __name__ == '__main__':
    app.run(debug=True)
