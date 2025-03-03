import pygame
import math
import time

WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (30, 30, 30)
SENSOR_COLOR = (0, 255, 0)
LASER_COLOR = (255, 0, 0)
MARK_COLOR = (255, 255, 0)
NUM_LASERS = 360
LASER_LENGTH = WIDTH

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# LiDAR
sensor_x, sensor_y = WIDTH // 2, HEIGHT // 2

# Obstacles
obstacles = [
    pygame.Rect(650, 250, 50, 100),
    pygame.Rect(150, 420, 50, 100),
    pygame.Rect(300, 100, 60, 120),
    pygame.Rect(500, 400, 80, 60),
    pygame.Rect(200, 200, 120, 40),
    pygame.Rect(0, 0, WIDTH, 5),
    pygame.Rect(0, HEIGHT - 5, WIDTH, 5),
    pygame.Rect(0, 0, 5, HEIGHT),
    pygame.Rect(WIDTH - 5, 0, 5, HEIGHT)
]

def cast_laser(sensor_x, sensor_y, angle, obstacles):
    """Casts a single laser and returns the point where it hits an obstacle (or max range)."""
    for i in range(LASER_LENGTH):
        x_check = int(sensor_x + math.cos(angle) * i)
        y_check = int(sensor_y + math.sin(angle) * i)
        
        for obstacle in obstacles:
            if obstacle.collidepoint(x_check, y_check):
                return x_check, y_check, i
    
    return sensor_x + math.cos(angle) * LASER_LENGTH, sensor_y + math.sin(angle) * LASER_LENGTH, LASER_LENGTH

running = True
marks = [] 
current_laser = 0 

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(BACKGROUND_COLOR)
    pygame.draw.circle(screen, SENSOR_COLOR, (sensor_x, sensor_y), 10)

    for obstacle in obstacles:
        pygame.draw.rect(screen, (100, 100, 100), obstacle)

    for mark in marks:
        pygame.draw.circle(screen, MARK_COLOR, mark, 5)

    # Fire one laser at a time
    if current_laser < NUM_LASERS:
        angle = math.radians(current_laser)
        laser_x, laser_y, distance = cast_laser(sensor_x, sensor_y, angle, obstacles)

        STEP_SIZE = 100  # Controls laser speed

        for step in range(0, distance, STEP_SIZE):
            screen.fill(BACKGROUND_COLOR)
            pygame.draw.circle(screen, SENSOR_COLOR, (sensor_x, sensor_y), 10)

            for obstacle in obstacles:
                pygame.draw.rect(screen, (100, 100, 100), obstacle)

            for mark in marks:
                pygame.draw.circle(screen, MARK_COLOR, mark, 5)

            laser_x_step = int(sensor_x + math.cos(angle) * step)
            laser_y_step = int(sensor_y + math.sin(angle) * step)
            pygame.draw.line(screen, LASER_COLOR, (sensor_x, sensor_y), (laser_x_step, laser_y_step), 1)

            pygame.display.flip()
            clock.tick(100)

        if distance < LASER_LENGTH and (laser_x, laser_y) not in marks:
            marks.append((laser_x, laser_y))

        for step in range(distance, 0, -STEP_SIZE):
            screen.fill(BACKGROUND_COLOR)
            pygame.draw.circle(screen, SENSOR_COLOR, (sensor_x, sensor_y), 10)

            for obstacle in obstacles:
                pygame.draw.rect(screen, (100, 100, 100), obstacle)

            for mark in marks:
                pygame.draw.circle(screen, MARK_COLOR, mark, 5)

            laser_x_step = int(laser_x - math.cos(angle) * (distance - step))
            laser_y_step = int(laser_y - math.sin(angle) * (distance - step))

            pygame.draw.line(screen, LASER_COLOR, (laser_x, laser_y), (laser_x_step, laser_y_step), 1)

            pygame.display.flip()
            clock.tick(100)

        current_laser += 1

    pygame.display.flip()
    clock.tick(10)

pygame.quit()