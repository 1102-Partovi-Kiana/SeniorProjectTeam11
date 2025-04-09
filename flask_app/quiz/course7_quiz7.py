quiz_data = {
    "questions": {
        "easy": [
            {
                "question": "What does the Fetch Pick and Place robot use to grab the object?",
                "options": [
                    "A suction cup",
                    "A magnetic clamp",
                    "A two-finger gripper",
                    "An extending spike"
                ],
                "answer": 2
            },
            {
                "question": "Which direction does the robot move in to align with the object horizontally?",
                "options": [
                    "Z direction",
                    "X and Y directions",
                    "Only Y direction",
                    "Randomly"
                ],
                "answer": 1
            },
            {
                "question": "What is the purpose of the `lift_action`?",
                "options": [
                    "To rotate the gripper",
                    "To raise the gripper vertically",
                    "To open the gripper",
                    "To pause the simulation"
                ],
                "answer": 1
            },
            {
                "question": "Which command is used to open the gripper?",
                "options": [
                    "env.step(close_grip_action)",
                    "env.open()",
                    "env.step(open_grip_action)",
                    "env.gripper.reset()"
                ],
                "answer": 2
            },
            {
                "question": "Which action happens first in the Pick and Place task?",
                "options": [
                    "Lower the gripper",
                    "Close the gripper",
                    "Lift the object",
                    "Open the gripper"
                ],
                "answer": 3
            }
        ],
        "medium": [
            {
                "question": "What is the purpose of the 'horizontal_distance_magnitude' in the movement logic?",
                "options": [
                    "It tells the robot which object to choose",
                    "It measures how far the gripper is from the box in X and Y",
                    "It sets the simulation time limit",
                    "It detects vertical misalignment"
                ],
                "answer": 1
            },
            {
                "question": "Why is the while loop used instead of a for loop when moving the gripper?",
                "options": [
                    "To simplify the math",
                    "Because it's shorter to write",
                    "Because we don’t know the exact number of steps needed",
                    "Because for loops don’t work with gripper data"
                ],
                "answer": 2
            },
            {
                "question": "Why do we pause the robot after closing the gripper?",
                "options": [
                    "To save power",
                    "To let the object stabilize in the grip",
                    "To recharge the robot",
                    "To update the simulation environment"
                ],
                "answer": 1
            },
            {
                "question": "Which component helps you measure if the gripper is above the object?",
                "options": [
                    "The gripper’s X coordinate",
                    "The Z-axis vertical distance",
                    "The object color",
                    "The simulation timer"
                ],
                "answer": 1
            },
            {
                "question": "What does this code do? `descend_action = np.array([0, 0, vertical_distance * 0.1, 0])`",
                "options": [
                    "Moves the gripper downward toward the object",
                    "Moves the object left and right",
                    "Closes the gripper with force",
                    "Rotates the entire robot arm"
                ],
                "answer": 0
            }
        ],
        "hard": [
            {
                "question": "Why do we normalize the horizontal direction vector before moving the gripper?",
                "options": [
                    "To remove negative values",
                    "To make sure the gripper moves a consistent step regardless of distance",
                    "To round the numbers to the nearest whole number",
                    "To avoid floating point errors"
                ],
                "answer": 1
            },
            {
                "question": "Why is `1e-8` added during normalization?",
                "options": [
                    "To increase speed of simulation",
                    "To avoid dividing by zero in case the distance is extremely small",
                    "To round the vector",
                    "To enhance camera tracking accuracy"
                ],
                "answer": 1
            },
            {
                "question": "When moving the object to the ball, why do we use the object’s position instead of the gripper’s?",
                "options": [
                    "The object is more accurate",
                    "The ball position is unknown",
                    "The goal is to move the object, not just the gripper",
                    "The gripper has no sensors"
                ],
                "answer": 2
            },
            {
                "question": "What does appending `0` as the fourth value in the action array represent?",
                "options": [
                    "Gripper force",
                    "No change in gripper open/close state",
                    "Signal to release the object",
                    "Time delay in movement"
                ],
                "answer": 1
            },
            {
                "question": "Which of the following would correctly stop the movement toward the goal?",
                "options": [
                    "`distance_from_object_to_ball < 1`",
                    "`np.mean(object_position) < 0.1`",
                    "`np.linalg.norm(object_position - ball_position) < distance_threshold`",
                    "`env.step(lift_action) == env.step(close_grip_action)`"
                ],
                "answer": 2
            }
        ]
    }
}
