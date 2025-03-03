import pygame
import math
import time

WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (30, 30, 30)
SENSOR_COLOR = (0, 255, 0)
LASER_COLOR = (255, 0, 0)
OBSTACLE_COLOR = (100, 100, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

sensor_x, sensor_y = WIDTH // 2, HEIGHT // 2
laser_angle1 = 0
laser_angle2 = 3*math.pi/4
laser_length = WIDTH 

obstacle1 = pygame.Rect(650, 250, 50, 100)
obstacle2 = pygame.Rect(150, 420, 50, 100)

def cast_laser(sensor_x, sensor_y, angle, obstacle):
    """Simulates laser emission and detects obstacle collision."""
    for i in range(laser_length):
        x_check = int(sensor_x + math.cos(angle) * i)
        y_check = int(sensor_y + math.sin(angle) * i)
        
        if obstacle.collidepoint(x_check, y_check):
            return x_check, y_check, i
    
    return sensor_x + math.cos(angle) * laser_length, sensor_y + math.sin(angle) * laser_length, laser_length

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(BACKGROUND_COLOR)
    
    pygame.draw.circle(screen, SENSOR_COLOR, (sensor_x, sensor_y), 15)
    
    pygame.draw.rect(screen, OBSTACLE_COLOR, obstacle1)
    pygame.draw.rect(screen, OBSTACLE_COLOR, obstacle2)
    
    laser_x1, laser_y1, distance1 = cast_laser(sensor_x, sensor_y, laser_angle1, obstacle1)
    laser_x2, laser_y2, distance2 = cast_laser(sensor_x, sensor_y, laser_angle2, obstacle2)
    
    angle1_degrees = math.degrees(laser_angle1)
    angle2_degrees = math.degrees(laser_angle2)
    
    start_time = time.time()
    
    for i in range(max(distance1, distance2)):
        screen.fill(BACKGROUND_COLOR)
        pygame.draw.circle(screen, SENSOR_COLOR, (sensor_x, sensor_y), 15)
        pygame.draw.rect(screen, OBSTACLE_COLOR, obstacle1)
        pygame.draw.rect(screen, OBSTACLE_COLOR, obstacle2)
        
        if i < distance1:
            laser_step_x1 = int(sensor_x + math.cos(laser_angle1) * i)
            laser_step_y1 = int(sensor_y + math.sin(laser_angle1) * i)
            pygame.draw.line(screen, LASER_COLOR, (sensor_x, sensor_y), (laser_step_x1, laser_step_y1), 4)
        
        if i < distance2:
            laser_step_x2 = int(sensor_x + math.cos(laser_angle2) * i)
            laser_step_y2 = int(sensor_y + math.sin(laser_angle2) * i)
            pygame.draw.line(screen, LASER_COLOR, (sensor_x, sensor_y), (laser_step_x2, laser_step_y2), 4)
        
        pygame.display.flip()
        clock.tick(120)
    
    print(f"Laser 1 (Angle: {angle1_degrees:.2f}°) - Distance: {distance1} pixels")
    print(f"Laser 2 (Angle: {angle2_degrees:.2f}°) - Distance: {distance2} pixels")
    
    time.sleep(0.1)
    
    for i in range(max(distance1, distance2), -1, -1):
        screen.fill(BACKGROUND_COLOR)
        pygame.draw.circle(screen, SENSOR_COLOR, (sensor_x, sensor_y), 15)
        pygame.draw.rect(screen, OBSTACLE_COLOR, obstacle1)
        pygame.draw.rect(screen, OBSTACLE_COLOR, obstacle2)
        
        if i < distance1:
            laser_step_x1 = int(sensor_x + math.cos(laser_angle1) * i)
            laser_step_y1 = int(sensor_y + math.sin(laser_angle1) * i)
            pygame.draw.line(screen, LASER_COLOR, (laser_x1, laser_y1), (laser_step_x1, laser_step_y1), 4)
        
        if i < distance2:
            laser_step_x2 = int(sensor_x + math.cos(laser_angle2) * i)
            laser_step_y2 = int(sensor_y + math.sin(laser_angle2) * i)
            pygame.draw.line(screen, LASER_COLOR, (laser_x2, laser_y2), (laser_step_x2, laser_step_y2), 4)
        
        pygame.display.flip()
        clock.tick(120)
    
    time_elapsed = time.time() - start_time
    print(f"Laser travel time: {time_elapsed:.4f} seconds")
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
