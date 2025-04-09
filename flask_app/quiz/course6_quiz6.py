quiz_data = {
    "questions": {
        "easy": [
            {
                "question": "What is the goal of the Fetch Reach robot?",
                "options": [
                    "Move blocks to a container",
                    "Pick up and sort colored blocks",
                    "Reach a destination point with its end-effector (gripper)",
                    "Map out its environment using LIDAR"
                ],
                "answer": 2
            },
            {
                "question": "What is the 'end-effector' on the Fetch Reach robot?",
                "options": [
                    "The robot’s base",
                    "The gripper at the tip of the arm",
                    "The camera module",
                    "The motor controller"
                ],
                "answer": 1
            },
            {
                "question": "Which toolkit is used to simulate the Fetch Reach robot?",
                "options": [
                    "PyTorch",
                    "Unity",
                    "OpenAI Gym",
                    "ROS2"
                ],
                "answer": 2
            },
           {
                "question": "What part of the Fetch Reach robot is responsible for interacting with objects?",
                "options": [
                    "The base",
                    "The sensors",
                    "The gripper (end-effector)",
                    "The antenna"
                ],
                "answer": 2
            },
            {
                "question": "What is the Fetch Reach simulation environment powered by?",
                "options": [
                    "Blender",
                    "MATLAB",
                    "MuJoCo",
                    "CoppeliaSim"
                ],
                "answer": 2
            }
        ],
        "medium": [
            {
                "question": "What does the 'distance_threshold' determine in the simulation?",
                "options": [
                    "The robot’s battery limit",
                    "How many steps the robot can take",
                    "How far the ball can move",
                    "When the gripper is close enough to the ball"
                ],
                "answer": 3
            },
            {
                "question": "What does the direction vector represent in the Fetch Reach simulation?",
                "options": [
                    "The rotation of the robot arm",
                    "The speed of the gripper",
                    "The path from the gripper to the ball",
                    "The amount of torque applied to the motor"
                ],
                "answer": 2
            },
            {
                "question": "How do you retrieve the ball’s position from the environment?",
                "options": [
                    "env.get_ball_location()",
                    "env.get_ball_position()",
                    "env.retrieve_ball_pos()",
                    "env.ball_coords()"
                ],
                "answer": 1
            },
            {
                "question": "Why is step size important in the gripper’s movement?",
                "options": [
                    "It sets the battery usage per step",
                    "It determines how far the gripper moves in each loop iteration",
                    "It limits the total number of movements allowed",
                    "It adjusts the gripper’s brightness"
                ],
                "answer": 1
            },
            {
                "question": "What does `env.step(action)` do?",
                "options": [
                    "Checks if the robot reached the goal",
                    "Reinitializes the robot’s state",
                    "Moves the gripper using the specified action",
                    "Prints the simulation results"
                ],
                "answer": 2
            }
        ],
        "hard": [
            {
                "question": "Why do we normalize the direction vector in the control logic?",
                "options": [
                    "To convert the direction into degrees",
                    "To make it compatible with OpenAI Gym",
                    "To have smooth, controlled movements of the gripper",
                    "To optimize for low battery usage"
                ],
                "answer": 2
            },
            {
                "question": "What is the purpose of appending `[1]` to the action vector?",
                "options": [
                    "To indicate completion of the task",
                    "To activate or stabilize the gripper",
                    "To normalize the direction vector",
                    "To apply torque to the motor"
                ],
                "answer": 1
            },
            {
                "question": "Why do we use a `while` loop instead of a `for` loop?",
                "options": [
                    "To save memory",
                    "Because the number of required steps is unknown",
                    "Because `for` loops are not supported in NumPy",
                    "To force the simulation to stop quickly"
                ],
                "answer": 1
            },
            {
                "question": "What function is used to calculate the magnitude of the direction vector?",
                "options": [
                    "np.add()",
                    "np.length()",
                    "np.linalg.norm()",
                    "np.vectorize()"
                ],
                "answer": 2
            },
            {
                "question": "Which condition correctly checks if the gripper has reached the ball?",
                "options": [
                    "direction < ball_position",
                    "distance_threshold == gripper_position",
                    "np.linalg.norm(direction) < distance_threshold",
                    "step_size > gripper_position"
                ],
                "answer": 2
            }
        ]
    }
}
