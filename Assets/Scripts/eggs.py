import pygame
import random

class Eggs():
    def __init__(self, loc, width, height, img, whoami) -> None:
        self.loc = loc
        self.width = width
        self.height = height
        self.img = img
        self.rect = pygame.rect.Rect(loc[0], loc[1], width, height)
        self.movement = [0,0]
        self.whoami = whoami
        self.collision_type = {}
        self.duplicate_x = 0
        self.duplicate_y = 0
    
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

    def update(self, tiles):
        self.movement = [0,0]
        self.movement[1] += 5
        self.collision_type = self.collision_checker(tiles)
    
    def draw(self, display, scroll):
        self.duplicate_x = self.rect.x 
        self.duplicate_y = self.rect.y
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        display.blit(self.img, self.rect)
        self.rect.x = self.duplicate_x
        self.rect.y = self.duplicate_y
    
    def get_rect(self):
        return self.rect

    def get_whoami(self):
        return self.whoami
