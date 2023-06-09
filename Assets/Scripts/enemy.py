import random
import math
import pygame
class Enemy():
    def __init__(self, loc, width, height, speed, shoot_cooldown, gun, enemy_costume, whoami, move = True, music = None) -> None:
        self.loc = loc
        self.width = width
        self.height = height
        self.rect = pygame.rect.Rect(loc[0], loc[1], width, height)
        self.shoot_cooldown = shoot_cooldown
        self.shoot_last_update = 0
        self.movement = []
        self.graviy = 9.8
        self.collision_type = {}
        self.display_x = 0
        self.display_y = 0
        self.gun = gun
        self.speed = speed
        self.bullets = []
        self.health = 100
        self.can_move = move
        self.enemy_costume = enemy_costume
        self.whoami = whoami
        self.start = False
        self.frame = 0
        self.music = music
        self.frame_last_update = 0
        self.frame_cooldown = 200
        self.facing_right = True
        if self.can_move == True:
            self.animation = 1
        else:
            self.animation = 0
    
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

    def draw_health_bar(self, display, health, x, y):
        x -= 25
        y -= 10
        ratio = health / 100
        pygame.draw.rect(display, (120,220,255), (x - 2, y - 2, 80  , 17//2))
        pygame.draw.rect(display, (255,0,0), (x, y, 76  , 15//2))
        pygame.draw.rect(display, (120,75,75), (x, y, 76 * ratio , 15//2))
    
    def move(self, angle, time, tiles, scroll, player_loc):
        self.movement = [0,0]
        self.bullets = self.gun.update(time, tiles)
        self.facing_right = self.gun.facing_direction()
        if self.gun.facing_direction():
            self.gun.rect.x = self.rect.x + 15
        else:
            self.gun.rect.x = self.rect.x - 15
        self.gun.rect.y = self.rect.y + 10
        if not self.start:
            distance_between = math.sqrt(math.pow((player_loc[0] - self.rect.x), 2) + math.pow((player_loc[1] - self.rect.y), 2))
            if distance_between < 350:
                self.start = True
        if self.start:
            if time - self.shoot_last_update > self.shoot_cooldown:
                self.gun.shoot((self.gun.rect.x - scroll[0], self.gun.rect.y - scroll[1]), self.gun.bullet_img.get_width(), self.gun.bullet_img.get_height(), angle, time, self.music)
                self.shoot_last_update = time
            if self.can_move:
                self.movement[0] += math.cos(angle) * self.speed
        self.movement[1] += self.graviy
        self.collision_type = self.collision_checker(tiles)
        if time - self.frame_last_update > self.frame_cooldown:
            self.frame += 1
            self.frame_last_update = time
        if self.frame >= 4:
            self.frame = 0
        return self.bullets
    
    def draw(self, display, scroll, angle):
        self.display_x = self.rect.x
        self.display_y = self.rect.y
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        self.draw_health_bar(display, self.health, self.rect.x, self.rect.y)
        #pygame.draw.rect(display, (0,0,0), self.rect)
        if self.facing_right:
            display.blit(self.enemy_costume[self.whoami][self.animation][self.frame], self.rect)
        else:
            flip = self.enemy_costume[self.whoami][self.animation][self.frame].copy()
            flip = pygame.transform.flip(flip, True, False)
            display.blit(flip, self.rect)
        self.rect.x = self.display_x
        self.rect.y = self.display_y
        self.gun.draw(display, scroll, angle)
    
    def get_rect(self):
        return self.rect

    def get_gun(self):
        return self.gun.get_gun()

    def destroy(self):
        del self.bullets