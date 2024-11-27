import os
import numpy as np
import mujoco_py

# Ensure we get the path separator correct on Windows
MODEL_XML_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 
    "venv38", 
    "lib", 
    "python3.8", 
    "site-packages", 
    "gym", 
    "envs", 
    "robotics", 
    "assets", 
    "car", 
    "car.xml"
)

DEFAULT_SIZE = 500

class CarEnv():
    def __init__(self):
        # Load the model and create the simulation
        self.model = mujoco_py.load_model_from_path(MODEL_XML_PATH)
        self.sim = mujoco_py.MjSim(self.model)
        self.viewer = None  # Will be initialized when rendering

    def get_car_position(self):
        car_id = self.sim.model.body_name2id('car')
        car_position = self.sim.data.body_xpos[car_id]
        return car_position

    def get_sensor_forward_value(self):
        sensor_id = self.sim.model.sensor_name2id('sensor_forward')
        return self.sim.data.sensordata[sensor_id]

    def get_sensor_right_value(self):
        sensor_id = self.sim.model.sensor_name2id('sensor_right')
        return self.sim.data.sensordata[sensor_id]

    def get_sensor_left_value(self):
        sensor_id = self.sim.model.sensor_name2id('sensor_left')
        return self.sim.data.sensordata[sensor_id]

    def get_sensor_backward_value(self):
        sensor_id = self.sim.model.sensor_name2id('sensor_backward')
        return self.sim.data.sensordata[sensor_id]

    def step(self, action):
        """
        Apply the action to the environment, step through simulation.
        
        Args:
            action (list or np.array): Action to apply (e.g., forward speed, turn speed).
        """
        # Apply action to the actuators (assuming action is a list of [forward, turn])
        forward, turn = action

        # Apply control input to motors (you may need to adjust this based on your action space)
        self.sim.data.ctrl[0] = forward  # forward motor
        self.sim.data.ctrl[1] = turn     # turning motor
        
        # Step the simulation forward
        self.sim.step()

    def render(self, mode='human', width=DEFAULT_SIZE, height=DEFAULT_SIZE):
        self._render_callback()  # Ensure this method is defined, even if empty
        if mode == 'rgb_array':
            self._get_viewer(mode).render(width, height)
            # window size used for old mujoco-py:
            data = self._get_viewer(mode).read_pixels(width, height, depth=False)
            # original image is upside-down, so flip it
            return data[::-1, :, :]
        elif mode == 'human':
            self._get_viewer(mode).render()

    def reset(self):
        """
        Reset the environment to its initial state.
        """
        self.sim.reset()
        return self.get_car_position()

    def _render_callback(self):
        """A custom callback before rendering. Can be used for custom visualizations."""
        pass  # No custom rendering behavior is required, so leave it empty.

    def _get_viewer(self, mode):
        if self.viewer is None:
            if mode == 'human':
                self.viewer = mujoco_py.MjViewer(self.sim)
            elif mode == 'rgb_array':
                self.viewer = mujoco_py.MjRenderContextOffscreen(self.sim, device_id=-1)
        return self.viewer

    def close(self):
        if self.viewer is not None:
            # self.viewer.finish()
            self.viewer = None
            self._viewers = {}


