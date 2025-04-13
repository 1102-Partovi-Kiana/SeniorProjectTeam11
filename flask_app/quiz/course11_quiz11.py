quiz_data = {
    "questions": {
        "easy": [
            {
                "question": "What is the primary purpose of the 'forward' sensor in the car environment?",
                "options": [
                    "To detect obstacles in front of the car",
                    "To measure the car's speed",
                    "To control the car's steering",
                    "To monitor the car's battery level"
                ],
                "answer": 0
            },
            {
                "question": "Which sensor is used to detect obstacles on the left side of the car?",
                "options": [
                    "Forward sensor",
                    "Right sensor",
                    "Left sensor",
                    "Temperature sensor"
                ],
                "answer": 2
            },
            {
                "question": "What action does the car take when the 'forward' sensor detects the greatest value?",
                "options": [
                    "Turn left",
                    "Turn right",
                    "Move forward",
                    "Stop completely"
                ],
                "answer": 2
            },
            {
                "question": "What does the code do when the car detects a collision?",
                "options": [
                    "It stops the car immediately",
                    "It checks for a success condition based on the collision object's color",
                    "It ignores the collision and continues moving",
                    "It reverses the car's direction"
                ],
                "answer": 1
            },
            {
                "question": "What is the role of the 'action' variable in the code?",
                "options": [
                    "It stores the car's current speed",
                    "It determines the car's next movement (e.g., turn left, turn right, move forward)",
                    "It measures the distance to the nearest obstacle",
                    "It tracks the car's battery usage"
                ],
                "answer": 1
            }
        ],
        "medium": [
            {
                "question": "How does the car decide which direction to turn when navigating?",
                "options": [
                    "By choosing a random direction",
                    "By following a pre-programmed path",
                    "By selecting the direction with the greatest sensor value",
                    "By waiting for user input"
                ],
                "answer": 2
            },
            {
                "question": "What happens if the 'left' sensor detects the greatest value?",
                "options": [
                    "The car turns left",
                    "The car turns right",
                    "The car moves forward",
                    "The car stops"
                ],
                "answer": 0
            },
            {
                "question": "What is the purpose of the 'time.sleep(0.0001)' statement in the code?",
                "options": [
                    "To slow down the simulation for better visualization",
                    "To speed up the car's movement",
                    "To reduce the sensor's accuracy",
                    "To stop the car temporarily"
                ],
                "answer": 0
            },
            {
                "question": "What does the 'success' variable indicate in the code?",
                "options": [
                    "The car has reached its destination",
                    "The car has collided with an obstacle",
                    "The car's battery is low",
                    "The car has detected a blue object"
                ],
                "answer": 3
            },
            {
                "question": "What is the significance of the 'target_color' in the collision detection logic?",
                "options": [
                    "It represents the color of the car",
                    "It is used to identify a specific object (e.g., a blue object) for success conditions",
                    "It determines the car's speed",
                    "It is used to change the car's color"
                ],
                "answer": 1
            }
        ],
        "hard": [
            {
                "question": "What does the 'max(values, key=values.get)' function do in the code?",
                "options": [
                    "It calculates the average sensor value",
                    "It determines the direction with the greatest sensor value",
                    "It stops the car when all sensors detect obstacles",
                    "It resets the sensor values"
                ],
                "answer": 1
            },
            {
                "question": "What is the purpose of the 'rgba' variable in the collision detection logic?",
                "options": [
                    "It stores the car's speed",
                    "It represents the color of the collided object",
                    "It measures the distance to the nearest obstacle",
                    "It tracks the car's battery level"
                ],
                "answer": 1
            },
            {
                "question": "How does the car handle a situation where all sensors detect obstacles at close range?",
                "options": [
                    "It stops and waits for assistance",
                    "It reverses or rotates to find a clear path",
                    "It speeds up to push through the obstacles",
                    "It ignores the obstacles and continues moving"
                ],
                "answer": 1
            },
            {
                "question": "What is the role of the 'geom1' and 'geom2' variables in the collision detection logic?",
                "options": [
                    "They store the car's sensor values",
                    "They represent the objects involved in a collision",
                    "They determine the car's speed",
                    "They track the car's position in the environment"
                ],
                "answer": 1
            },
            {
                "question": "What is the purpose of the 'np.array_equal(color, target_color)' function in the code?",
                "options": [
                    "It checks if the car's speed matches a target value",
                    "It compares the color of the collided object to the target color (blue)",
                    "It calculates the distance to the nearest obstacle",
                    "It determines the car's next movement direction"
                ],
                "answer": 1
            }
        ]
    }
}
