# Base Code: https://www.youtube.com/watch?v=JbUNsYPJK1U

import math
import pygame
class buildEnvironment:
    def __init__(self,MapDimensions):
        pygame.init()
        self.pointCloud=[]
        self.externalMap=pygame.image.load('map4.bmp')
        self.maph, self.mapw = MapDimensions
        self.MapWindowName = 'LiDar Sensor Map'
        pygame.display.set_caption(self.MapWindowName)
        self.map = pygame.display.set_mode((self.mapw, self.maph))
        self.map.blit(self.externalMap,(0,0))
        # Colors
        self.black = (0,0,0)
        self.grey = (70,70,70)
        self.Blue = (0,0,255)
        self.Green = (0,255,0)
        self.Red = (255,0,0)
        self.white = (255,255,255)

    def AD2pos(self,distance,angle,robotPosition):
        x = distance * math.cos(angle)+robotPosition[0]
        y = -distance * math.sin(angle)+robotPosition[1]
        return (int(x), int(y))
    
    def dataStorage(self,data):

        print(len(self.pointCloud))
        for element in data:
            point=self.AD2pos(element[0],element[1],element[2])
            if point not in self.pointCloud:
                self.pointCloud.append(point)

    def show_sensorData(self):
        self.infomap = self.map.copy() 
        for point in self.pointCloud:
            pygame.draw.circle(self.infomap, (255, 0, 0), (int(point[0]), int(point[1])), 3)
