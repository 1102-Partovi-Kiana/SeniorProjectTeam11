import os
from gym import utils
from gym.envs.robotics import fetch_env


# Ensure we get the path separator correct on windows
MODEL_XML_PATH = "/mnt/c/Users/kpartovi/Desktop/CS425/SeniorProjectTeam11/venv38/lib/python3.8/site-packages/gym/envs/robotics/assets/fetch/organize.xml"


class FetchOrganizeEnv(fetch_env.FetchEnv, utils.EzPickle):
    def __init__(self, reward_type='sparse'):
        initial_qpos = {
            'robot0:slide0': 0.405,
            'robot0:slide1': 0.48,
            'robot0:slide2': 0.0,
            'object0:joint': [1.25, 0.8, 0.4, 1., 0., 0., 0.],  # Position of first block
            'object1:joint': [1.3, 0.6, 0.4, 1., 0., 0., 0.],  # Position of second block
            'object2:joint': [1.35, 1, 0.4, 1., 0., 0., 0.],  # Position of third block
            'object3:joint': [1.4, 0.6, 0.4, 1., 0., 0., 0.],  # Position of third block
        }
       
        # Initialize FetchEnv with the model XML, including the objects and robot setup
        fetch_env.FetchEnv.__init__(
            self, MODEL_XML_PATH, has_object=True, block_gripper=False, n_substeps=20,
            gripper_extra_height=0.2, target_in_the_air=True, target_offset=0.0,
            obj_range=0.15, target_range=0.15, distance_threshold=0.05,
            initial_qpos=initial_qpos, reward_type=reward_type)
        utils.EzPickle.__init__(self)
   
    def get_ball_position(self):
        """Returns the position of the target (ball or object to be picked)"""
        ball_id = self.sim.model.site_name2id('target0')
        ball_position = self.sim.data.site_xpos[ball_id]
        return ball_position


    def get_gripper_position(self):
        """Returns the position of the gripper"""
        gripper_geom_id = self.sim.model.site_name2id('robot0:grip')
        gripper_position = self.sim.data.geom_xpos[gripper_geom_id]
        return gripper_position
   
    def get_box_position(self, box_name='object0'):
        """Returns the position of a specified object (block)"""
        object_position = self.sim.data.get_site_xpos(box_name)
        return object_position




