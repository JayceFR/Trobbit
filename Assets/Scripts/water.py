import pygame
from pygame.locals import *
import math
import random
class Water():
    def __init__(self,x,y,width,height, radius) -> None:
        self.x = x 
        self.y = y
        self.width = width
        self.height = height
        self.radius = radius
        self.molecules = []
        self.molecule_pos = []
        self.collision_cooldown = 1000
        self.collision_last_update = 0
        for x in range(width//radius):
            self.molecules.append(Molecule(self.x, self.y, self.radius))
            self.x += self.radius * 2
        self.max_size = len(self.molecules)
        self.width = self.x + self.radius
        self.collide_particle = 0

    def chain_call(self, display, scroll, player_rect, time):
        self.molecule_pos = []
        detuct = 50
        for pos, molecule in enumerate(self.molecules):
            if molecule.get_rect().colliderect(player_rect):
                self.colliding(pos, time)
            if molecule.energy_transfer == True:
                molecule.energy_transfer = False
                if pos + 1 < len(self.molecules) and pos >= self.collide_particle:
                    self.molecules[pos+1].colliding = True
                    #self.molecules[pos+1].tension = self.molecules[pos].final - detuct - random.randint(1,20)
                if pos - 1 >= 0 and pos <= self.collide_particle:
                    self.molecules[pos - 1].colliding = True
                    #self.molecules[pos - 1].tension = self.molecules[pos].final - detuct - random.randint(1,20)
            molecule.oscillation()
            self.molecule_pos.append(list((molecule.get_x() - scroll[0], molecule.get_y() - scroll[1])))
            self.molecule_pos.append(list((molecule.get_x() - scroll[0], self.y + self.height - scroll[1])))
            molecule.draw(display, scroll)
        self.molecule_pos.append(list((self.molecules[0].get_x() - scroll[0], self.y+self.height - scroll[1])))
        #self.molecule_pos.append(list((self.molecules[0].get_x() - 5, self.molecules[0].get_y() + 20)))
        #self.molecule_pos.append(list((self.molecules[len(self.molecules)-1].get_x() + 5, self.molecules[len(self.molecules)-1].get_y() + 20)))
        pygame.draw.polygon(display, (15,161,227), self.molecule_pos, 10)

    def colliding(self, pos, time):
        if time - self.collision_last_update > self.collision_cooldown:
            if not self.molecules[pos].colliding:
                self.collide_particle = pos
                self.molecules[pos].colliding = True
            self.collision_last_update = time
    
class Molecule():
    def __init__(self, x ,y, radius) -> None:
        self.x = x
        self.y = y
        self.rect = pygame.rect.Rect(x,y,radius,radius)
        self.final = y
        self.radius = radius
        self.colliding = False
        self.energy_transfer = False
        self.tension = y - 10
        self.angle = 0
        self.original_stage = y
        
    
    def oscillation(self):
        if self.colliding:
            self.y -= math.sin(math.radians(self.angle)) * 50
            self.angle = 50
            if self.angle > 360:
                self.angle = 0
            if self.y < self.tension:
                self.colliding = False
                self.energy_transfer = True
        if not self.colliding:
            self.angle = 0
            if self.y < self.original_stage:
                self.y += 5
            self.tension = self.y - 50 
    
    def draw(self, display, scroll):
        pygame.draw.circle(display, (15,161,227), (self.x - scroll[0], self.y - scroll[1]), self.radius)
    
    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_rect(self):
        return self.rect
    
    def collision(self):
        self.colliding = True

