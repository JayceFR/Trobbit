import pygame
import math
import json

f = open("./Assets/Data/bg_coordinates.json", "r")
y = f.read()
f.close()
class background():
    def __init__(self) -> None:
        self.coordinates = json.loads(y)['coordinates']
        self.bars = []
        for coordinate in self.coordinates:
            self.bars.append(Bars(coordinate))
        
    def recursive_call(self, display):
        for pos, bar in sorted(enumerate(self.bars), reverse=True):
            bar.move()
            bar.draw(display)

class Bars():
    def __init__(self, coordinate) -> None:
        self.coordinate = coordinate
        self.visible = True
    
    def move(self):
        for coordinate in self.coordinate:
            coordinate[1] -= 1
            if coordinate[1] < -50:
                self.visible = False
            if self.visible == False:
                self.coordinate = [[0,380], [500,350], [500,365], [0,395]]
                self.visible = True
    
    def draw(self, display):
        pygame.draw.polygon(display, (157,225,255), self.coordinate)
    
    def change_coordinate(self, coordinate):
        self.coordinate = coordinate
    
    def change_visible(self, what):
        self.visible = what
    