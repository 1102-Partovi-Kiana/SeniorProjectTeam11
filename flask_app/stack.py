import os
from gym import utils
from gym.envs.robotics import fetch_env


# Ensure we get the path separator correct on windows
MODEL_XML_PATH = "/mnt/c/Users/kpartovi/Desktop/CS425/SeniorProjectTeam11/venv38/lib/python3.8/site-packages/gym/envs/robotics/assets/fetch/stack.xml"


class FetchStackEnv(fetch_env.FetchEnv, utils.EzPickle):
    def __init__(self, reward_type='sparse'):
        initial_qpos = {
            'robot0:slide0': 0.405,
            'robot0:slide1': 0.48,
            'robot0:slide2': 0.0,
            'object0:joint': [1.25, 0.8, 0.4, 1., 0., 0., 0.],  # Position of first block
            'object1:joint': [1.3, 0.6, 0.4, 1., 0., 0., 0.],  # Position of second block
            'object2:joint': [1.35, 1, 0.4, 1., 0., 0., 0.],  # Position of third block
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


    def check_stacking_success(env, box_positions, stack_threshold=0.01, height_threshold=0.05):
        """
        Check if boxes are stacked successfully.
       
        Parameters:
        - env: Simulation environment.
        - box_positions: List of site names for the boxes (e.g., ['object0', 'object1', 'object2']).
        - stack_threshold: Maximum allowable horizontal misalignment (x, y).
        - height_threshold: Minimum height difference to consider boxes stacked.
       
        Returns:
        - bool: True if all boxes are successfully stacked, False otherwise.
        """
        for i in range(len(box_positions) - 1):
            box1_position = env.sim.data.get_site_xpos(box_positions[i])
            box2_position = env.sim.data.get_site_xpos(box_positions[i + 1])
           
            # Check horizontal alignment (x, y)
            horizontal_distance = np.linalg.norm(box1_position[:2] - box2_position[:2])
            if horizontal_distance > stack_threshold:
                print(f"Boxes {box_positions[i]} and {box_positions[i + 1]} are misaligned: {horizontal_distance:.4f}")
                return False
           
            # Check vertical stacking (z)
            height_difference = box2_position[2] - box1_position[2]
            if abs(height_difference - height_threshold) > stack_threshold:
                print(f"Boxes {box_positions[i]} and {box_positions[i + 1]} have incorrect height difference: {height_difference:.4f}")
                return False
       
        print("All boxes are successfully stacked!")
        return True