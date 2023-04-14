import pygame
import random

class Fab():
    def __init__(self, loc, width, height, img) -> None:
        self.loc = loc
        self.width = width
        self.height = height
        self.rect = pygame.rect.Rect(loc[0], loc[1], width, height)
        self.movement = [0,0]
        self.collison_type = {}
        self.display_x = 0
        self.display_y = 0
        self.in_use = False
        self.alive = True
        self.img = img
        self.health_cooldown = 100
        self.health_last_update = 0

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

    def update(self, tiles, time, player):
        self.movement = [0,0]
        self.movement[1] += 5
        self.collision_checker(tiles)
        if self.in_use:
            if time - self.health_last_update > self.health_cooldown:
                if player.health <= 100:
                    player.health += 5
                self.health_last_update = time
            if player.health >= 100:
                self.alive = False
                self.in_use = False

    
    def draw(self, display, scroll):
        self.display_x = self.rect.x
        self.display_y = self.rect.y
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        display.blit(self.img, self.rect)
        self.rect.y = self.display_y
        self.rect.x = self.display_x
    
    def get_rect(self):
        return self.rect

    def use(self):
        if self.alive:
            self.in_use = True
    
    def get_use(self):
        return self.in_use

    
    def facing_direction(self):
        return True