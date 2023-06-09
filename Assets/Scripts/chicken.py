import pygame

class Chicken():
    def __init__(self, loc, width, height, animaiton_idle, facing_right) -> None:
        self.rect = pygame.rect.Rect(loc[0], loc[1], width, height)
        self.frame = 0
        self.animation_idle = animaiton_idle
        self.frame_last_update = 0
        self.frame_cooldown = 200
        self.facing_right = facing_right
        self.display_x = 0
        self.display_y = 0
        self.movement = [0,0]
        self.collision_type = {}
    
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
    
    def update(self, tiles, time):
        self.movement = [0,0]
        self.movement[1] += 5
        self.collision_type = self.collision_checker(tiles)
        if time - self.frame_last_update > self.frame_cooldown:
            self.frame_last_update = time
            self.frame += 1
            if self.frame > 3:
                self.frame = 0
    
    def draw(self, display, scroll):
        self.display_x = self.rect.x
        self.display_y = self.rect.y
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        if self.facing_right:
            flip = self.animation_idle[self.frame].copy()
            flip = pygame.transform.flip(flip, True, False)
            display.blit(flip, self.rect)
        else:
            display.blit(self.animation_idle[self.frame], self.rect)
        self.rect.x = self.display_x
        self.rect.y = self.display_y
    
    def get_rect(self):
        return self.rect
            
