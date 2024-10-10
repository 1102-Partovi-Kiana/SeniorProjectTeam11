from flask import Flask, render_template, Response, request, redirect, url_for
import gym
import cv2

app = Flask(__name__)

# Create the Gym environment
env = gym.make("FetchReach-v1")
env.reset()

def generate_frames():
    while True:
        frame = env.render(mode='rgb_array')
        obs, reward, done, info = env.step(env.action_space.sample())
        if done:
            env.reset()

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        ret, buffer = cv2.imencode('.jpg', frame)

        if not ret:
            continue

        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/echo', methods=['POST'])
def echo():
    user_input = request.form.get('input', '')
    
    # Print the input to the command prompt
    print(f"User typed: {user_input}")

    # Redirect back to home after submission
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)