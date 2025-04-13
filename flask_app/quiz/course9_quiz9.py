quiz_data = {
    "questions": {
        "easy": [
            {
                "question": "What is the primary task of the Fetch Organize Robot?",
                "options": [
                    "To sort objects by size",
                    "To detect, pick, and sort colored blocks into the correct container",
                    "To race across a platform",
                    "To play music while moving objects"
                ],
                "answer": 1
            },
            {
                "question": "Which environment object is used for this simulation?",
                "options": [
                    "FetchReachEnv",
                    "FetchPickAndPlaceEnv",
                    "FetchOrganizeEnv",
                    "FetchSortEnv"
                ],
                "answer": 2
            },
            {
                "question": "Which array opens the gripper in the simulation?",
                "options": [
                    "descend_action",
                    "close_grip_action",
                    "open_grip_action",
                    "release_action"
                ],
                "answer": 2
            },
            {
                "question": "How many target-colored blocks does the robot need to sort?",
                "options": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "answer": 1
            },
            {
                "question": "Which direction is used to lift the gripper?",
                "options": [
                    "X-axis",
                    "Y-axis",
                    "Z-axis",
                    "W-axis"
                ],
                "answer": 2
            }
        ],
        "medium": [
            {
                "question": "What does the variable `gripper_to_object_distance_threshold` represent?",
                "options": [
                    "The weight of the object",
                    "The time allowed to complete a task",
                    "The minimum distance before grasping the object",
                    "The color of the target container"
                ],
                "answer": 2
            },
            {
                "question": "Why is color detection important in the Fetch Organize task?",
                "options": [
                    "It activates the robot’s motors",
                    "It helps the robot identify which blocks to sort",
                    "It changes the robot's path",
                    "It synchronizes with the simulation clock"
                ],
                "answer": 1
            },
            {
                "question": "Which of the following methods retrieves the object’s color?",
                "options": [
                    "env.get_color()",
                    "env.color.read('object')",
                    "env.sim.model.geom_rgba[geom_id]",
                    "env.retrieve_color(object_id)"
                ],
                "answer": 2
            },
            {
                "question": "What happens if the object's color doesn't match the target color?",
                "options": [
                    "It gets destroyed",
                    "The robot releases it and returns to start",
                    "It’s placed in a random location",
                    "The robot paints it the correct color"
                ],
                "answer": 1
            },
            {
                "question": "What is `direction_to_container` used for?",
                "options": [
                    "To identify object weight",
                    "To normalize the robot’s color filters",
                    "To move the object towards the container",
                    "To rotate the camera view"
                ],
                "answer": 2
            }
        ],
        "hard": [
            {
                "question": "Why do we normalize direction vectors in movement logic?",
                "options": [
                    "To keep actions at a consistent scale regardless of distance",
                    "To avoid floating point errors",
                    "To make simulation faster",
                    "To align with camera perspective"
                ],
                "answer": 0
            },
            {
                "question": "Which variable represents a small downward movement?",
                "options": [
                    "lift_action",
                    "grip_action",
                    "descend_action",
                    "drag_down_action"
                ],
                "answer": 2
            },
            {
                "question": "What does the fourth value of `0` in an action array like `[x, y, z, 0]` signify?",
                "options": [
                    "Release gripper",
                    "Pause simulation",
                    "No change to the gripper state",
                    "End the loop"
                ],
                "answer": 2
            },
            {
                "question": "How is the color of an object retrieved in the simulation?",
                "options": [
                    "Using `geom_name2id` and accessing `geom_rgba`",
                    "Calling `env.get_color()` directly",
                    "Using `env.color_id()`",
                    "Accessing the object through `sim.camera.read_color()`"
                ],
                "answer": 0
            },
            {
                "question": "What is the stopping condition when the object is close enough to the container?",
                "options": [
                    "`env.sim.is_near_container(object)`",
                    "`np.linalg.norm(object_position - container_position) <= container_to_object_distance_threshold`",
                    "`object_position.mean() > 0.1`",
                    "`env.step(open_grip_action) == True`"
                ],
                "answer": 1
            }
        ]
    }
}
