quiz_data = {
    "questions": {
        "easy": [
            {
                "question": "What is the main task of the Fetch robot in this context?",
                "options": [
                    "Navigate a maze",
                    "Stack three blocks on top of each other",
                    "Sort blocks by color",
                    "Deliver objects to different locations"
                ],
                "answer": 1
            },
            {
                "question": "Which component of the Fetch robot is used to pick up and stack blocks?",
                "options": [
                    "The robotic arm and gripper",
                    "The robot’s wheels",
                    "The robot’s camera",
                    "The robot’s base"
                ],
                "answer": 0
            },
            {
                "question": "What is the main challenge in stacking blocks using Fetch?",
                "options": [
                    "Balancing the blocks correctly",
                    "Finding the blocks",
                    "Detecting different block colors",
                    "Moving at high speed"
                ],
                "answer": 0
            },
            {
                "question": "Which part of the Fetch robot’s code is responsible for its movements?",
                "options": [
                    "The motion planning module",
                    "The visualization engine",
                    "The battery management system",
                    "The user interface"
                ],
                "answer": 0
            },
            {
                "question": "What happens if the gripper does not fully close on a block?",
                "options": [
                    "The block may slip or fall",
                    "The robot will move faster",
                    "The simulation will stop",
                    "The block will change color"
                ],
                "answer": 0
            }
        ],
        "medium": [
            {
                "question": "What type of motion is required for the Fetch robot to stack blocks accurately?",
                "options": [
                    "Precise arm articulation and gripper control",
                    "Fast and continuous movements",
                    "Randomized movements",
                    "Pre-programmed block placements"
                ],
                "answer": 0
            },
            {
                "question": "How does the simulation determine the position of each block?",
                "options": [
                    "Using world coordinates (x, y, z)",
                    "By tracking colors",
                    "Through a random function",
                    "By manually placing them"
                ],
                "answer": 0
            },
            {
                "question": "What is an important factor when gripping a block for stacking?",
                "options": [
                    "Gripper force and positioning",
                    "Block weight only",
                    "Robot’s battery level",
                    "Block color"
                ],
                "answer": 0
            },
            {
                "question": "What is the role of `env.step()` in the Fetch stacking task?",
                "options": [
                    "Advance the simulation and update the robot’s state",
                    "Reset the block positions",
                    "Manually move the blocks",
                    "Generate new blocks"
                ],
                "answer": 0
            },
            {
                "question": "Why is simulation useful for training a Fetch robot to stack blocks?",
                "options": [
                    "It allows testing without physical hardware",
                    "It removes the need for robot programming",
                    "It makes the robot faster",
                    "It automatically improves the robot’s skills"
                ],
                "answer": 0
            }
        ],
        "hard": [
            {
                "question": "How is the Fetch robot’s arm movement typically controlled in the simulation?",
                "options": [
                    "By specifying joint positions with `env.step()`",
                    "By manually adjusting the robot’s arm",
                    "By dragging blocks with the mouse",
                    "By setting a fixed path for the arm"
                ],
                "answer": 0
            },
            {
                "question": "Which Python module is commonly used to simulate the Fetch robot stacking blocks?",
                "options": [
                    "`gym` or `mujoco-py`",
                    "`numpy`",
                    "`matplotlib`",
                    "`os`"
                ],
                "answer": 0
            },
            {
                "question": "How does the robot determine if a block is successfully stacked?",
                "options": [
                    "By checking the block’s position relative to the stack",
                    "By measuring the block’s weight",
                    "By detecting the block’s color",
                    "By checking if the gripper is open"
                ],
                "answer": 0
            },
            {
                "question": "Why is it important to define initial values for blocks in the simulation?",
                "options": [
                    "To set their starting positions correctly",
                    "To improve simulation speed",
                    "To prevent robot movement errors",
                    "To add visual effects"
                ],
                "answer": 0
            },
            {
                "question": "What method should be used to release a block when stacking?",
                "options": [
                    "Gradually opening the gripper while maintaining block stability",
                    "Immediately dropping the block from a height",
                    "Throwing the block using fast gripper movement",
                    "Using a function that teleports the block to the correct position"
                ],
                "answer": 0
            }
        ]
    }
}