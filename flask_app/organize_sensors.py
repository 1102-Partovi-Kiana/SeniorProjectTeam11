# Darren's Code
import os
from gym import utils
from gym.envs.robotics import fetch_env
import numpy as np

# This path is specific for 'venv38' virtual environment
MODEL_XML_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
    "venv38", 
    "lib", 
    "python3.8", 
    "site-packages", 
    "gym", 
    "envs", 
    "robotics", 
    "assets", 
    "fetch", 
    "organize_with_sensors.xml"
)
class FetchOrganizeSensorsEnv(fetch_env.FetchEnv, utils.EzPickle):
    def __init__(self, reward_type='sparse'):
        initial_qpos = {
            'robot0:slide0': 0.5049,
            'robot0:slide1': 0.48,
            'robot0:slide2': 0,
            'object0:joint': [1.3, 0.8, 0.4, 1., 0., 0., 0.],  # Position of first block
            'object1:joint': [1.3, 0.55, 0.4, 1., 0., 0., 0.],  # Position of second block
            'object2:joint': [1.45, .95, 0.4, 1., 0., 0., 0.],  # Position of third block
            'object3:joint': [1.45, 0.65, 0.4, 1., 0., 0., 0.],  # Position of third block
        }
        fetch_env.FetchEnv.__init__(
            self, MODEL_XML_PATH, has_object=False, block_gripper=False, n_substeps=20,
            gripper_extra_height=0.2, target_in_the_air=False, target_offset=0.0,
            obj_range=0.15, target_range=0.15, distance_threshold=0.05,
            initial_qpos=initial_qpos, reward_type=reward_type)
        utils.EzPickle.__init__(self)

    def get_ball_position(self):
        ball_id = self.sim.model.site_name2id('target0')
        ball_position = self.sim.data.site_xpos[ball_id]
        return ball_position

    def get_gripper_position(self):
        gripper_geom_id = self.sim.model.site_name2id('robot0:grip')
        gripper_position = self.sim.data.geom_xpos[gripper_geom_id]
        return gripper_position 
    
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

# End of Darren's Code