# Base Code: https://www.youtube.com/watch?v=JbUNsYPJK1U

import env
import sensors
import pygame
import math
import random

environment = env.buildEnvironment((600, 1200))
environment.originalMap = environment.map.copy()
laser = sensors.LaserSensor(50, environment.originalMap, uncertainty=(0.01, 0, 0.01))
environment.map.fill((0, 0, 0))
environment.infomap = environment.map.copy()

robot_image = pygame.image.load("robot.bmp")
robot_rect = robot_image.get_rect()

robot_position = [500, 400]
robot_speed = 2
robot_angle = math.pi / 2
total_pixels = environment.maph * environment.mapw

future_steps = 15

def is_valid_position(x, y):
    if x <= 0 or x >= 1200 or y <= 0 or y >= 600:
        return False
    color = environment.originalMap.get_at((int(x), int(y)))
    return color == (255, 255, 255, 255)

running = True

while running:
    environment.map.fill((0, 0, 0)) 
    environment.map.blit(environment.infomap, (0, 0)) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_x = robot_position[0]
    current_y = robot_position[1]
    next_x = robot_position[0] + robot_speed * math.cos(robot_angle)
    next_y = robot_position[1] - robot_speed * math.sin(robot_angle)

    collision_detected = False
    for step in range(1, future_steps + 1):
        future_x = current_x + step * robot_speed * math.cos(robot_angle)
        future_y = current_y - step * robot_speed * math.sin(robot_angle)

        if not is_valid_position(future_x, future_y):
            collision_detected = True
            break

    print(current_x, ",", current_y, ",", environment.originalMap.get_at((int(current_x), int(current_y))))

    if not collision_detected:
        robot_position[0] = next_x
        robot_position[1] = next_y
    else:
        robot_angle += math.pi / 2

    laser.position = tuple(robot_position)
    sensor_data = laser.sense_obstacles()

    environment.dataStorage(sensor_data)
    environment.show_sensorData()

    explored_percentage = len(environment.pointCloud) / total_pixels
    print(f"Explored: {explored_percentage * 100:.2f}%")
    if explored_percentage >= 0.0032:
        print("Stopping the simulation.")
        running = False

    if current_x <= 0 or current_x >= 1200 or current_y <= 0 or current_y >= 600:
        running = False

    robot_rect.center = (int(robot_position[0]), int(robot_position[1]))
    environment.map.blit(robot_image, robot_rect)

    pygame.display.flip()

pygame.quit()