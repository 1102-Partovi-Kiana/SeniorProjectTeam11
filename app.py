from flask import Flask, render_template
import gym
import numpy as np
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)

# Create the Gym environment
env = gym.make("FetchReach-v1")
env.reset()

def encode_frame(frame):
    # Convert the frame (numpy array) to a PIL Image
    image = Image.fromarray(frame)
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    # Encode the image as base64
    return base64.b64encode(buffer.read()).decode('utf-8')

@app.route('/')
def home():
    frames = []
    for _ in range(100):  # Reduce the number of frames for demonstration
        frame = env.render(mode='rgb_array')  # Capture RGB array frame
        encoded_frame = encode_frame(frame)  # Encode frame to base64
        frames.append(encoded_frame)

        # Perform a random action for demonstration
        obs, reward, done, info = env.step(env.action_space.sample())
        if done:
            env.reset()

    return render_template('index.html', frames=frames)

if __name__ == '__main__':
    app.run(debug=True)