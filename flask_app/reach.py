import os
from gym import utils
from gym.envs.robotics import fetch_env

# Path for general devices
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
    "reach.xml"
)

# Darren's Code
class ReachEnv(fetch_env.FetchEnv, utils.EzPickle):
    def __init__(self, reward_type='sparse'):
        initial_qpos = {
            'robot0:slide0': 0.4049,
            'robot0:slide1': 0.48,
            'robot0:slide2': 0.0,
        }
        fetch_env.FetchEnv.__init__(
            self, MODEL_XML_PATH, has_object=False, block_gripper=True, n_substeps=20,
            gripper_extra_height=0.2, target_in_the_air=False, target_offset=0.0,
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
    
# End of Darren's Code