import random
import pygame
import math

class Player():
    def __init__(self, x,y,width,height, player_img, idle_animation, run_animation, land_img, music = None):
        self.rect = pygame.Rect(x,y,width,height)
        self.display_x = 0
        self.width = width
        self.life = 0
        self.height = height
        self.alive = True
        self.music = music
        self.display_y = 0 
        self.moving_left = False
        self.moving_right = False
        self.facing_left = False
        self.facing_right = True
        self.land_img = land_img
        self.movement = [0,0]
        self.player_img = player_img.copy()
        self.player_img = pygame.transform.scale(self.player_img, (player_img.get_width()*2, player_img.get_height()*2))
        self.player_img.set_colorkey((0,0,0))
        self.idle_animation = idle_animation
        self.run_animation = run_animation
        self.frame = 0 
        self.frame_last_update = 0
        self.frame_cooldown = 200
        self.gravity = 5
        self.jump = False
        self.jump_last_update = 0
        self.jump_cooldown = 600
        self.jump_up_spped = 10
        self.air_timer = 0
        self.collision_type = {}
        self.in_air = False
        self.recover = False
        self.recover_cooldown = 500
        self.recover_last_update = 0
        self.dusts = []
        self.health = 100
        self.speed = 5
        self.acceleration = 0.02
        self.deceleration = 0.2
    
    def draw_health_bar(self, display, health, x, y):
        ratio = health / 100
        pygame.draw.rect(display, (0,0,0), (x - 2, y - 2, 204  , 36//2))
        pygame.draw.rect(display, (255,255,255), (x, y, 200  , 28//2))
        if health > 50:
            pygame.draw.rect(display, (0,255,0), (x, y, 200 * ratio , 28//2))
        elif health > 25 and health <= 50:
            pygame.draw.rect(display, (255,255,0), (x, y, 200 * ratio , 28//2))
        else:
            pygame.draw.rect(display, (255,0,0), (x, y, 200 * ratio , 28//2))


    def draw(self, window, scroll, img = None):
        self.display_x = self.rect.x
        self.display_y = self.rect.y
        self.rect.x = self.rect.x - scroll[0]
        self.rect.y = self.rect.y - scroll[1]
        self.draw_health_bar(window, self.health, 2, 2 )
        #if self.recover:
        #    window.blit(self.land_img, self.rect)
        if img != None:
            window.blit(img, self.rect)
        else:
            if not self.moving_left and  not self.moving_right:
                if self.facing_right:
                    if self.recover:
                        window.blit(self.land_img, self.rect)
                    else:
                        window.blit(self.idle_animation[self.frame], self.rect)

                else:
                    if self.recover:
                        flip = self.land_img.copy()
                        flip = pygame.transform.flip(self.land_img, True, False)
                        flip.set_colorkey((0,0,0))
                    else:
                        flip = self.idle_animation[self.frame].copy()
                        flip = pygame.transform.flip(self.idle_animation[self.frame], True, False)
                        flip.set_colorkey((0,0,0))
                    window.blit(flip, self.rect)
            else:
                if self.facing_right:
                    window.blit(self.run_animation[self.frame], self.rect)
                else:
                    flip = self.run_animation[self.frame].copy()
                    flip = pygame.transform.flip(self.run_animation[self.frame], True, False)
                    flip.set_colorkey((0,0,0))
                    window.blit(flip, self.rect)
        
        #pygame.draw.rect(window, (255,255,0), self.rect)
        self.rect.x = self.display_x
        self.rect.y = self.display_y

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

    def move(self, tiles, time, dt, display, scroll, gun, facing_right, pistol = None, shield = False, can_move = True):
        self.movement = [0, 0]
        if self.health > 100:
            self.health = 100
        if (self.moving_left or self.moving_right) and not self.jump:
            #self.speed += self.acceleration
            if self.speed > 8:
                self.speed = 8
            self.frame_cooldown -= self.deceleration
            if self.frame_cooldown < 100:
                self.frame_cooldown = 100
        else:
            self.speed = 5
            self.frame_cooldown = 200
        if self.moving_right:
            self.movement[0] += self.speed * dt 
            self.moving_right = False
            if self.facing_left:
                self.facing_right = True
                self.facing_left = False
        if self.moving_left:
            self.movement[0] -= self.speed * dt
            self.moving_left = False
            if self.facing_right:
                self.facing_left = True
                self.facing_right = False
        if self.jump:
            if self.air_timer < 40:
                self.air_timer += 1
                self.movement[1] -= self.jump_up_spped
                self.jump_up_spped -= 0.5
            else:
                self.air_timer = 0
                self.jump = False
                self.jump_up_spped = 10

        #Frame
        if time - self.frame_last_update > self.frame_cooldown:
            self.frame += 1
            if self.frame > 3:
                self.frame = 0
            self.frame_last_update = time

        key = pygame.key.get_pressed()
        if can_move:
            if key[pygame.K_LEFT] or key[pygame.K_a]:
                self.moving_left = True
            if key[pygame.K_RIGHT] or key[pygame.K_d]:
                self.moving_right = True
            if key[pygame.K_SPACE] or key[pygame.K_w]:
                if not self.jump and self.collision_type['bottom']:
                    if time - self.jump_last_update > self.jump_cooldown:
                        self.music.play()
                        self.jump = True
                        self.jump_last_update = time
        
        if not self.jump:
            self.movement[1] += self.gravity

        self.collision_type = self.collision_checker(tiles)

        if pistol != None:
            if self.facing_right:
                if not shield:
                    pistol.rect.x = self.rect.x
                else:
                    pistol.facing_right = True
                    pistol.rect.x = self.rect.x + 17
            else:
                if not shield:
                    pistol.rect.x = self.rect.x - 8
                else:
                    pistol.facing_right = False
                    pistol.rect.x = self.rect.x - 7
            if not shield:
                pistol.rect.y = self.rect.y + 15
            else:
                pistol.rect.y = self.rect.y 

        if self.collision_type['bottom']:
            if self.in_air:
                #Just Landed
                self.recover = True
                self.recover_last_update = time
                self.dusts.append(Dust((self.rect.x + self.width//2, self.rect.y + self.height), time , 120))
            self.in_air = False
        else:
            self.in_air = True
        
        if self.recover:
            if time - self.recover_last_update > self.recover_cooldown:
                self.recover = False
        
        for pos, dust in sorted(enumerate(self.dusts), reverse=True):
            if not dust.alive:
                self.dusts.pop(pos)
            else:
                dust.draw(display, time, scroll)
        if gun:
            if facing_right:
                self.facing_right = True
                self.facing_left = False
            else:
                self.facing_left = True
                self.facing_right = False


    def get_rect(self):
        return self.rect

    def right_facing(self):
        return self.facing_right
#Map 
class Map():
    def __init__(self, map_loc, tiles, tree):
        self.map = [] 
        self.tiles = tiles
        self.tree = tree
        f = open(map_loc, "r")
        data = f.read()
        f.close()
        data = data.split("\n")
        for row in data:
            self.map.append(list(row))
    
    def blit_map(self, window, scroll, left_click_img, numbers_img, right_click_img, space_img, wasd_img):
        x = 0
        y = 0 
        tile_rects = []
        grass_loc = []
        pistol_loc = []
        smg_loc = []
        rocket_loc = []
        menemy_loc = []
        qenemy_loc = []
        shield_loc = []
        water_loc = []
        fab_loc = []
        egg_loc = []
        player_loc = []
        for row in self.map:
            x = 0 
            for element in row:
                if element != "t" and element != "g" and element != "0" and element != "p" and element != "s" and element != "r" and element != "e" and element != "l" and element != "w" and element != "f" and element != "m" and element != "q" and element != "e" and element != "x":
                    window.blit(self.tiles[int(element)-1], (x * 32 - scroll[0], y * 32 - scroll[1]))
                if element == "t":
                    window.blit(self.tree, (x * 32 - scroll[0] - 90, y * 32 - scroll[1] - 150))
                if element == "g":
                    grass_loc.append((x*32, y*32))
                if element == "p":
                    pistol_loc.append((x*32, y*32))
                if element == "s":
                    smg_loc.append((x*32,y*32))
                if element == "r":
                    rocket_loc.append((x*32, y*32))
                if element == "l":
                    shield_loc.append((x*32,y*32))
                if element == "e":
                    egg_loc.append((x*32, y*32))
                if element == "w":
                    water_loc.append((x*32,y*32))
                if element == "m":
                    menemy_loc.append((x*32,y*32))
                if element == "q":
                    qenemy_loc.append((x*32,y*32))
                if element == "f":
                    fab_loc.append((x*32,y*32))
                if element == "x":
                    player_loc.append((x*32, y*32))
                if element != "0" and element != "t" and element != "g" and element != "p" and element != "s" and element != "r" and element != "e" and element != "l" and element != "w" and element != "f" and element != "m" and element != "q" and element != "e" and element != "x":
                    tile_rects.append(pygame.rect.Rect(x*32,y*32,32,32))
                x += 1
            y += 1
        return tile_rects, grass_loc, pistol_loc, smg_loc, rocket_loc, menemy_loc, qenemy_loc, shield_loc, water_loc, fab_loc, egg_loc, player_loc


class Glow():
    def __init__(self, loc):
        self.master_glow = []
        for x in range(30):
            self.master_glow.append(Circles(loc[0] + random.randint(-30,30), loc[1] + random.randint(-30,30), random.randint(5,20), random.randint(50,70), random.randint(-2,2)))

    def update(self, time, display, scroll):
        for glow in self.master_glow:
            glow.draw(display, scroll)
            glow.move(time)

class Dust():
    def __init__(self, loc, time, death_after_time) -> None:
        self.loc = loc
        self.master_dust = []
        self.start_time = time
        self.alive = True
        self.death_after_time = death_after_time
        for x in range(15):
            self.master_dust.append(Circles(loc[0]+ random.randint(-10,10), loc[1] + random.randint(-5,5), random.randint(1,4), random.randint(0,10), random.randint(-2,2), (100,100,100)))

    def draw(self, display, time, scroll):
        if time - self.start_time > self.death_after_time:
            self.alive = False
        for dust in self.master_dust:
            dust.move(time)
            dust.draw(display, scroll)

class Smoke():
    def __init__(self, loc, color = (255,255,255)) -> None:
        self.loc = loc
        self.circles = []
        for x in range(8):
            self.circles.append(Circles(loc[0] + random.randint(-20, 20), loc[1] + random.randint(-20,20), random.randint(1,8), random.randint(1000,2000), 0.5, color, 1, math.radians(random.randint(0,360))))
    
    def draw(self, display, scroll, time):
        for pos, circle in sorted(enumerate(self.circles), reverse=True):
            circle.draw(display, scroll)
            circle.move(time)
            if circle.radius < 0:
                self.circles.pop(pos)

class Enchanted():
    def __init__(self, loc) -> None:
        self.loc = loc
        self.circles = []
    
    def update(self,loc):
        self.loc = loc
        for x in range(5):
            self.circles.append(Circles(loc[0] + random.randint(0,20), loc[1] + random.randint(-20,20), random.randint(2,4), random.randint(1000, 2000), 0.2, (234,63,247), 2, math.radians(random.randint(0,360))))
    
    def draw(self,time, display, scroll, color = None):
        for pos, circle in sorted(enumerate(self.circles), reverse=True):
            if color == None:
                circle.draw(display, scroll)
            else:
                circle.draw(display, scroll, color)
            circle.move(time)
            if circle.radius < 0:
                self.circles.pop(pos)


class Circles():
    def __init__(self,x,y,radius, cooldown, dradius, color = (207,207,207), type = 0, angle=0) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.max_radius = radius + radius * 0.5
        self.min_radius = radius - radius * 0.5
        self.last_update = 0
        self.cooldown = cooldown
        self.angle = angle
        self.dradius = dradius
        self.type = type
        self.color = color
        
    
    def move(self, time):
        if self.type == 0:
            if time - self.last_update > self.cooldown:
                self.radius += self.dradius
                if self.radius > self.max_radius:
                    self.dradius *= -1
                if self.radius < self.min_radius:
                    self.dradius *= -1
                self.last_update = time
        if self.type == 1:
            if time - self.last_update > self.cooldown:
                self.radius -= self.dradius
                self.x += math.cos(self.angle) * 5
                self.y += math.sin(self.angle) * 5
                self.y += 0.7
        if self.type == 2:
            if time - self.last_update > self.cooldown:
                self.radius -= self.dradius
                self.x += math.cos(self.angle) * 5
                self.y -= 1.7
    
    def update_angle(self):
        angle = math.degrees(self.angle)
        angle += random.randint(0,30)
        if angle > 360:
            angle = 0
        self.angle = math.radians(angle)
    

    def draw(self, display, scroll, color = None):
        if color == None:
            pygame.draw.circle(display, self.color, (self.x - scroll[0], self.y - scroll[1]),self.radius)
        else:
            pygame.draw.circle(display, color, (self.x - scroll[0], self.y - scroll[1]),self.radius)
