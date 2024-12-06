import os
from gym import utils
from gym.envs.robotics import fetch_env

# Path for general devices
MODEL_XML_PATH = os.path.join('fetch', 'pick_and_place.xml')

# Darren's Code
class FetchPickAndPlaceEnv(fetch_env.FetchEnv, utils.EzPickle):
    def __init__(self, reward_type='sparse'):
        initial_qpos = {
            'robot0:slide0': 0.405,
            'robot0:slide1': 0.48,
            'robot0:slide2': 0.0,
            'object0:joint': [1.25, 0.8, 0.4, 1., 0., 0., 0.],
        }
        fetch_env.FetchEnv.__init__(
            self, MODEL_XML_PATH, has_object=True, block_gripper=False, n_substeps=20,
            gripper_extra_height=0.2, target_in_the_air=True, target_offset=0.0,
            obj_range=0.15, target_range=0.15, distance_threshold=0.05,
            initial_qpos=initial_qpos, reward_type=reward_type)
        utils.EzPickle.__init__(self)

    
    def get_ball_position(self):
        ball_id = self.sim.model.site_name2id('target0')
        ball_position = self.sim.data.site_xpos[ball_id]
        return ball_position

    def get_gripper_position(self):
        gripper_geom_id = self.sim.model.geom_name2id('robot0:l_gripper_finger_link')
        gripper_position = self.sim.data.geom_xpos[gripper_geom_id]
        return gripper_position 
    
    def get_box_position(self):
        object_position = self.sim.data.get_site_xpos('object0')
        return object_position

# End of Darren's Code