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
    for i in range(LASER_LENGTH):
        x_check = int(sensor_x + math.cos(angle) * i)
        y_check = int(sensor_y + math.sin(angle) * i)
        
        for obstacle in obstacles:
            if obstacle.collidepoint(x_check, y_check):
                return x_check, y_check, i
    
    return sensor_x + math.cos(angle) * LASER_LENGTH, sensor_y + math.sin(angle) * LASER_LENGTH, LASER_LENGTH

running = True
marks = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(BACKGROUND_COLOR)
    pygame.draw.circle(screen, SENSOR_COLOR, (sensor_x, sensor_y), 10)

    laser_points = []
    laser_distances = []
    laser_data = []
    laser_times = []

    for i in range(NUM_LASERS):
        angle = math.radians(i)
        laser_x, laser_y, distance = cast_laser(sensor_x, sensor_y, angle, obstacles)
        laser_points.append((laser_x, laser_y))
        laser_distances.append(distance)
        return_time = distance / LASER_LENGTH
        laser_times.append(return_time)
        laser_data.append((i, distance, return_time))
        
        if distance < LASER_LENGTH:
            if (laser_x, laser_y) not in marks:
                marks.append((laser_x, laser_y))
    
    for step in range(max(laser_distances)):
        screen.fill(BACKGROUND_COLOR)
        pygame.draw.circle(screen, SENSOR_COLOR, (sensor_x, sensor_y), 10)
        
        for i in range(NUM_LASERS):
            if step < laser_distances[i]:
                laser_x = int(sensor_x + math.cos(math.radians(i)) * step)
                laser_y = int(sensor_y + math.sin(math.radians(i)) * step)
                pygame.draw.line(screen, LASER_COLOR, (sensor_x, sensor_y), (laser_x, laser_y), 1)
            else:
                laser_x, laser_y = laser_points[i]
                pygame.draw.line(screen, LASER_COLOR, (sensor_x, sensor_y), (laser_x, laser_y), 1)

            pygame.draw.circle(screen, SENSOR_COLOR, (sensor_x, sensor_y), 10)
        
        pygame.display.flip()
        clock.tick(60)
    
    time.sleep(0.3)
    
    for step in range(max(laser_distances)):
        screen.fill(BACKGROUND_COLOR)
        pygame.draw.circle(screen, SENSOR_COLOR, (sensor_x, sensor_y), 10)

        for mark in marks:
            pygame.draw.circle(screen, MARK_COLOR, mark, 5)
        
        for i in range(NUM_LASERS):
            if step < laser_distances[i]:
                laser_x = int(laser_points[i][0] - math.cos(math.radians(i)) * (step))
                laser_y = int(laser_points[i][1] - math.sin(math.radians(i)) * (step))
                pygame.draw.line(screen, LASER_COLOR, (laser_points[i][0], laser_points[i][1]), (laser_x, laser_y), 1)
            else:
                pygame.draw.line(screen, LASER_COLOR, (laser_points[i][0], laser_points[i][1]), (sensor_x, sensor_y), 1)

            pygame.draw.circle(screen, SENSOR_COLOR, (sensor_x, sensor_y), 10)
        
        pygame.display.flip()
        clock.tick(60)
    
    for angle, distance, return_time in laser_data:
        print(f"Angle: {angle}°, Distance: {distance}px, Return Time: {return_time:.4f}s")
    
    pygame.display.flip()
    clock.tick(10)

pygame.quit()
