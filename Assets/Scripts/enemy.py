import random
import math
import pygame
class Enemy():
    def __init__(self, loc, width, height, shoot_cooldown) -> None:
        self.loc = loc
        self.width = width
        self.height = height
        self.rect = pygame.rect.Rect(loc[0], loc[1], width, height)
        self.shoot_cooldown = shoot_cooldown
        self.shoot_last_update = 0
        self.movement = []
        self.graviy = 9.8
        self.speed = 5
        self.collision_type = {}
        self.display_x = 0
        self.display_y = 0
    
    def collision_test(self, tiles):
        hitlist = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hitlist.append(tile)
        return hitlist
    
    def collision_checker(self, tiles):
        collision_types = {"top": False, "bottom": False, "right": False, "left": False}
        self.rect.x += self.movement[0]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.movement[0] > 0:
                self.rect.right = tile.left
                collision_types["right"] = True
            elif self.movement[0] < 0:
                self.rect.left = tile.right
                collision_types["left"] = True
        self.rect.y += self.movement[1]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.movement[1] > 0:
                self.rect.bottom = tile.top
                collision_types["bottom"] = True
            if self.movement[1] < 0:
                self.rect.top = tile.bottom
                collision_types["top"] = True
        return collision_types
    
    def move(self, angle, time, tiles):
        self.movement = [0,0]
        if time - self.shoot_last_update > self.shoot_cooldown:
            self.shoot_last_update = time
        self.movement[0] += math.cos(angle) * self.speed
        self.movement[1] += self.graviy
        self.collision_type = self.collision_checker(tiles)
    
    def draw(self, display, scroll):
        self.display_x = self.rect.x
        self.display_y = self.rect.y
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        pygame.draw.rect(display, (0,0,0), self.rect)
        self.rect.x = self.display_x
        self.rect.y = self.display_y
    
    def get_rect(self):
        return self.rect