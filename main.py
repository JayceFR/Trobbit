#TODO -> Mkae explosion for rocket launcher
#TODO -> Add Med Kit and chicken
#TODO -> Good Level Design
#TODO -> Make enemies a bit weak

import pygame 
import time as t
import random
import math
import Assets.Scripts.framework as f
import Assets.Scripts.background as backg
import Assets.Scripts.bg_particles as bg_particles
import Assets.Scripts.grass as g
import Assets.Scripts.pistol as pistol
import Assets.Scripts.smg as smg
import Assets.Scripts.rocket as rocket
import Assets.Scripts.sparks as spark
import Assets.Scripts.enemy as enemy
pygame.init()
from pygame.locals import *

#Getting image from spirtesheet
def get_image(sheet, frame, width, height, scale, colorkey):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(colorkey)
    return image

def blit_grass(grasses, display, scroll, player):
    for grass in grasses:
        if grass.get_rect().colliderect(player.get_rect()):
            grass.colliding()
        grass.draw(display, scroll)

def blit_inventory(display, inventory, font, item_dict, item_slot):
    left = 400
    pygame.draw.line(display, (255,255,255), (left - 10, 300), (left, 270))
    pygame.draw.line(display, (255,255,255), (left, 270), (500, 270))
    for x in range(len(inventory)):
        if item_slot == x:
            pygame.draw.rect(display, (0,150,0), pygame.rect.Rect(left, 275, 20, 20), border_radius=5)    
        else:
            pygame.draw.rect(display, (150,0,0), pygame.rect.Rect(left, 275, 20, 20), border_radius=5)
        draw_text(str(x+1), font, (255,255,255), left + 9, 294, display)
        pygame.draw.rect(display, (0,0,0), pygame.rect.Rect(left + 2, 275 + 2.5, 20 - 2.5, 20 - 2.5), border_radius=4)
        if item_dict.get(inventory[x]) != None:
            if item_dict[inventory[x]][0] == "Pistol":
                display.blit(item_dict[inventory[x]][1], (left + 3, 275 + 3.5))
            if item_dict[inventory[x]][0] == "SMG":
                display.blit(item_dict[inventory[x]][1], (left + 3, 275 + 3.5))
            if item_dict[inventory[x]][0] == "Rocket":
                display.blit(item_dict[inventory[x]][1], (left + 3, 275 + 3.5))
        left += 25

def draw_text(text, font, text_col, x, y, display):
    img = font.render(text, True, text_col)
    display.blit(img, (x, y))

def free_inventory_slot(inventory):
    for x in range(len(inventory)):
        if inventory[x] == "":
            return x
    return "full"

#Display settings 
screen_w = 1000
screen_h = 600
window = pygame.display.set_mode((screen_w,screen_h))
display = pygame.Surface((screen_w//2, screen_h//2))
pygame.display.set_caption("TROBBIT")
#Game Attributes
run = True
clock = pygame.time.Clock()
#Loading Images
tiles = []
for x in range(9):
    current_tile = pygame.image.load("./Assets/Tiles/tile{tile_pos}.png".format(tile_pos = str(x+1))).convert_alpha()
    tile_dup = current_tile.copy()
    tile_dup = pygame.transform.scale(tile_dup, (32,32))
    tiles.append(tile_dup)
player_img = pygame.image.load("./Assets/Sprites/player_img.png").convert_alpha()
player_idle_img = pygame.image.load("./Assets/Sprites/player_idle.png").convert_alpha()
player_run_img = pygame.image.load("./Assets/Sprites/player_run.png").convert_alpha()
player_land_img_copy = pygame.image.load("./Assets/Sprites/player_land.png").convert_alpha()
player_land_img = player_land_img_copy.copy()
player_land_img = pygame.transform.scale(player_land_img_copy, (player_land_img_copy.get_width() * 1.5, player_land_img_copy.get_height() * 1.5))
player_land_img.set_colorkey((0,0,0))
tree_img_copy = pygame.image.load("./Assets/Sprites/tree.png").convert_alpha()
tree_img = tree_img_copy.copy()
tree_img = pygame.transform.scale(tree_img_copy, (tree_img_copy.get_width()*3.5, tree_img_copy.get_height()*2.7))
tree_img.set_colorkey((0,0,0))
pistol_img = pygame.image.load("./Assets/Entities/pistol.png").convert_alpha()
pistol_img.set_colorkey((0,0,0))
smg_img = pygame.image.load("./Assets/Entities/smg.png").convert_alpha()
smg_img = pygame.transform.scale(smg_img, (smg_img.get_width()*1.5, smg_img.get_height()*1.5))
smg_img.set_colorkey((0,0,0))
rocketb_img = pygame.image.load("./Assets/Entities/rocketb.png").convert_alpha()
rocketb_img = pygame.transform.scale(rocketb_img, (rocketb_img.get_width()*2.5, rocketb_img.get_height()*2.5))
rocketb_img.set_colorkey((0,0,0))
rocket_img = pygame.image.load("./Assets/Entities/rocket.png").convert_alpha()
rocket_img = pygame.transform.scale(rocket_img, (rocket_img.get_width()*2.5, rocket_img.get_height()*2.5))
rocket_img.set_colorkey((0,0,0))
rocket_ammo_img = pygame.image.load("./Assets/Entities/rocket_ammo.png").convert_alpha()
rocket_ammo_img = pygame.transform.scale(rocket_ammo_img, (rocket_ammo_img.get_width()*2, rocket_ammo_img.get_height()*2))
rocket_ammo_img.set_colorkey((0,0,0))
bullet_img = pygame.image.load("./Assets/Entities/bullet.png").convert_alpha()
bullet_img.set_colorkey((255,255,255))
smg_bullet_img = pygame.image.load("./Assets/Entities/smg_bullet.png").convert_alpha()
pistol_logo_img = pistol_img.copy()
pistol_logo_img = pygame.transform.scale(pistol_logo_img, (pistol_logo_img.get_width()//2, pistol_img.get_height()//2))
pistol_logo_img = pygame.transform.rotate(pistol_logo_img, 45)
smg_logo_img = smg_img.copy()
smg_logo_img = pygame.transform.scale(smg_logo_img, (smg_logo_img.get_width()//2, smg_logo_img.get_height()//2))
smg_logo_img = pygame.transform.rotate(smg_logo_img, 45)
rocket_logo_img = pygame.image.load("./Assets/Entities/rocket.png").convert_alpha()
rocket_logo_img = pygame.transform.scale(rocket_logo_img, (rocket_logo_img.get_width()//1.5, rocket_logo_img.get_height()//1.5))
rocket_logo_img = pygame.transform.rotate(rocket_logo_img, 45)
#Grass
grasses = []
grass_loc = []
grass_spawn = True
grass_last_update = 0
grass_cooldown = 50
#Map
map = f.Map("./Assets/Maps/map.txt",tiles,tree_img)
#Player settings
player_idle_animation = []
player_x = 0
player_y = 0
player_run_animation = []
for x in range(4):
    player_idle_animation.append(get_image(player_idle_img, x, 23, 37, 1.5, (0,0,0)))
for x in range(4):
    player_run_animation.append(get_image(player_run_img, x, 23, 37, 1.5, (0,0,0)))
player = f.Player(30,30,player_idle_animation[0].get_width(),player_idle_animation[0].get_height(), player_img, player_idle_animation, player_run_animation, player_land_img)
#Random Variables
true_scroll = [0,0]
scroll = [0,0]
last_time = t.time()
#Mouse Settings
pygame.mouse.set_visible(False)
#Fonts
inven_font = pygame.font.Font("./Assets/Fonts/jayce.ttf", 5)
pick_up_font = pygame.font.Font("./Assets/Fonts/jayce.ttf", 15)
#lightings
glow_effects = []
for x in range(150):
    glow_effects.append(f.Glow((random.randint(-1000, 3000), random.randint(-100,700))))
#Enchanted Particles
enchanted = f.Enchanted([0,0])
#background stripes
bg = backg.background()
bg_particle_effect = bg_particles.Master()
#Inventory
inventory = ["", "", "", ""]
inventory_items = {"0": None, "1": None, "2": None, "3": None}    #{'0' : pistol_object}
inven_slot = -1
#Rocket
rocket_locs = []
rockets = []
rocket_spawn = True
#SMG
smg_locs = []
smgs = []
smg_spawn = True
#Pistol
angle = 0
smg_spray = False
pistol_locs = []
pistols = []
smg_cooldown = 100
pistol_spawn = True
smg_last_update = 0
bullets = []
sparks = []
smokes = []
yeagle = pistol.Pistol((35, 45), pistol_img.get_width(), pistol_img.get_height(), pistol_img, bullet_img)
#Dictionary Of Items
item_dict = {"p" : ["Pistol", pistol_logo_img, -2], "s" : ["SMG", smg_logo_img, -2], "r" : ["Rocket", rocket_logo_img, -2]}
#Enemy
enemies = []
enemy_spawn = True
enemy_angle = 0
enemy_bullets = []
enemy_locs = []
enemy_count = 0
#Main Game Loop
while run:
    clock.tick(60)
    key = pygame.key.get_pressed()
    dt = t.time() - last_time
    dt *= 60
    last_time = t.time()
    time = pygame.time.get_ticks()
    display.fill((157,225,255))
    #VFX
    for glow_effect in glow_effects:
        glow_effect.update(time, display, scroll)
    bg.recursive_call(display)
    #Mouse Settings 
    mpos = pygame.mouse.get_pos()
    #Blitting the Map
    tile_rects, grass_loc, pistol_locs, smg_locs, rocket_locs, enemy_locs = map.blit_map(display, scroll)
    #Creating Items
    if grass_spawn:
        for loc in grass_loc:
            x_pos = loc[0]
            while x_pos < loc[0] + 32:
                x_pos += 2.5
                grasses.append(g.grass([x_pos, loc[1]+14], 2, 18))
        grass_spawn = False
    if enemy_spawn:           
        for loc in enemy_locs:
            choice = random.randint(1,3)
            cooldown = [0,0]
            if choice == 1:
                gun = pistol.Pistol(loc, pistol_img.get_width(), pistol_img.get_height(), pistol_img, bullet_img)
                cooldown = [1000, 2000]
            elif choice == 2:
                gun = smg.SMG(loc, smg_img.get_width(), smg_img.get_height(), smg_img, smg_bullet_img)
                cooldown = [100, 300]
            else:
                gun = rocket.Rocket(loc,rocket_img.get_width(), rocket_img.get_height(), rocketb_img, rocket_img, rocket_ammo_img)
                cooldown = [1000, 2000]
            enemies.append(enemy.Enemy(loc, 32, 32, random.randint(2,7), random.randint(cooldown[0],cooldown[1]), gun ))
        enemy_spawn = False
    if rocket_spawn:
        for loc in rocket_locs:
            rockets.append(rocket.Rocket(loc, rocketb_img.get_width(), rocketb_img.get_height(), rocketb_img, rocket_img, rocket_ammo_img))
        rocket_spawn = False
    if smg_spawn:
        for loc in smg_locs:
            smgs.append(smg.SMG(loc, smg_img.get_width(), smg_img.get_height(), smg_img, smg_bullet_img))
        smg_spawn = False
    if pistol_spawn:
        for loc in pistol_locs:
            pistols.append(pistol.Pistol(loc, pistol_img.get_width(), pistol_img.get_height(), pistol_img, bullet_img))
        pistol_spawn = False
    #Movement of grass
    if time - grass_last_update > grass_cooldown:
        for grass in grasses:
            grass.move()
        grass_last_update = time
    #Drawing pistols
    for position, p in sorted(enumerate(pistols), reverse=True):
        if p.get_rect().colliderect(player.get_rect()):
            #pop up e
            draw_text("E",pick_up_font, (255,255,255), p.get_rect().x - scroll[0] + 16, p.get_rect().y - 16 - scroll[1], display )
            if key[pygame.K_e]:
                pos = free_inventory_slot(inventory)
                if pos != "full" and item_dict["p"][2] < 0:
                    inventory[pos] = "p"
                    item_dict["p"][2] = pos
                    inventory_items[str(pos)] = p
                    pistols.pop(position)
        p.draw(display, scroll, 0)
        p.update(time, tile_rects)
    #Drawing smgs
    for position, p in sorted(enumerate(smgs), reverse=True):
        if p.get_rect().colliderect(player.get_rect()):
            #pop up e
            draw_text("E",pick_up_font, (255,255,255), p.get_rect().x - scroll[0] + 16, p.get_rect().y - 16 - scroll[1], display )
            if key[pygame.K_e]:
                pos = free_inventory_slot(inventory)
                if pos != "full" and item_dict["s"][2] < 0:
                    inventory[pos] = "s"
                    item_dict["s"][2] = pos
                    inventory_items[str(pos)] = p
                    smgs.pop(position)
        p.draw(display, scroll, 0)
        p.update(time, tile_rects)
    #Drawing Rockets
    for position, p in sorted(enumerate(rockets), reverse=True):
        if p.get_rect().colliderect(player.get_rect()):
            #pop up e
            draw_text("E",pick_up_font, (255,255,255), p.get_rect().x - scroll[0] + 16, p.get_rect().y - 16 - scroll[1], display )
            if key[pygame.K_e]:
                pos = free_inventory_slot(inventory)
                if pos != "full" and item_dict["r"][2] < 0:
                    inventory[pos] = "r"
                    item_dict["r"][2] = pos
                    inventory_items[str(pos)] = p
                    rockets.pop(position)
        p.draw(display, scroll, 0)
        p.update(time, tile_rects)
    #Drawing enemies
    for position, e in sorted(enumerate(enemies), reverse=True):
        enemy_angle = math.atan2(( (e.get_rect().y - scroll[1]) - (player.get_rect().y - scroll[1])) , ( (e.get_rect().x - scroll[0]) - (player.get_rect().x - scroll[0])))
        enemy_angle = math.pi - enemy_angle
        enemy_bullets = e.move(enemy_angle, time, tile_rects, scroll)
        e.draw(display, scroll, enemy_angle)
        #Checking for collisions with player
        for bullet in enemy_bullets:
            bullet_x = bullet.get_rect().x
            bullet_y = bullet.get_rect().y
            bullet.get_rect().x += scroll[0]
            bullet.get_rect().y += scroll[1]
            if bullet.get_rect().colliderect(player.get_rect()):
                player.health -= 10
                for x in range(30):
                    if bullet.get_gun() == "r":
                        sparks.append(spark.Spark([bullet_x , bullet_y], math.radians(random.randint(0,360)), random.randint(7,14), (255,103,20 ), 2, 1))
                    else:
                        sparks.append(spark.Spark([bullet_x , bullet_y], math.radians(random.randint(0,360)), random.randint(2,7), (255,103,20), 0.5, 1))
                bullet.alive = False
            bullet.get_rect().x = bullet_x
            bullet.get_rect().y = bullet_y
        for bullet in bullets:
            bullet_x = bullet.get_rect().x
            bullet_y = bullet.get_rect().y
            bullet.get_rect().x += scroll[0]
            bullet.get_rect().y += scroll[1]
            if bullet.get_rect().colliderect(e.get_rect()):
                if bullet.get_gun() == "r":
                    e.health -= 70
                if bullet.get_gun() == "p":
                    e.health -= 30
                if bullet.get_gun() == "s":
                    e.health -= 10
                for x in range(30):
                    if bullet.get_gun() == "r":
                        sparks.append(spark.Spark([bullet_x , bullet_y], math.radians(random.randint(0,360)), random.randint(7,14), (255,103,20 ), 2, 1))
                    else:
                        sparks.append(spark.Spark([bullet_x , bullet_y], math.radians(random.randint(0,360)), random.randint(2,7), (255,103,20), 0.5, 1))
                bullet.alive = False
            bullet.get_rect().x = bullet_x
            bullet.get_rect().y = bullet_y
        if e.health <= 0:
            e.destroy()
            enemies.pop(position)
    #Calculating Scroll
    true_scroll[0] += (player.get_rect().x - true_scroll[0] - 262) / 5
    true_scroll[1] += (player.get_rect().y - true_scroll[1] - 162) / 5
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])
    #Smg Spray Shoot
    if smg_spray:
        if time - smg_last_update > smg_cooldown:
            inventory_items[str(inven_slot)].shoot((player_x - scroll[0], player_y - scroll[1]), bullet_img.get_width(), bullet_img.get_height(), angle, time)
            smg_last_update = time   
    #Inventory Calculation
    if key[pygame.K_1]:
        inven_slot = 0
    if key[pygame.K_2]:
        inven_slot = 1
    if key[pygame.K_3]:
        inven_slot = 2
    if key[pygame.K_4]:
        inven_slot = 3
    blit_inventory(display, inventory, inven_font, item_dict, inven_slot)
    if player.right_facing():
        player_x = player.get_rect().x + 22
        player_y = player.get_rect().y + 15
    else:
        player_x = player.get_rect().x - 1
        player_y = player.get_rect().y + 15
    #Angle Calculation
    angle = math.atan2(( mpos[1]//2 - (player_y - scroll[1])) , (mpos[0]//2 - (player.get_rect().x - scroll[0])))
    angle *= -1
    if inventory_items.get(str(inven_slot)) != None:
        if inventory[inven_slot] == "p" or inventory[inven_slot] == "s" or inventory[inven_slot] == "r":
            inventory_items[str(inven_slot)].draw(display, scroll, angle)
            bullets = inventory_items[str(inven_slot)].update(time, tile_rects)
    for tile in tile_rects:
        for bullet in bullets:
            bullet_x = bullet.get_rect().x
            bullet_y = bullet.get_rect().y
            bullet.get_rect().x += scroll[0]
            bullet.get_rect().y += scroll[1]
            if tile.colliderect(bullet.get_rect()):
                bullet.alive = False
                for x in range(30):
                    if bullet.get_gun() == "r":
                        sparks.append(spark.Spark([bullet_x , bullet_y], math.radians(random.randint(0,360)), random.randint(7,14), (255,255,255), 2, 1))
                    else:
                        smokes.append(f.Smoke((bullet_x + scroll[0], bullet_y + scroll[1])))

            bullet.get_rect().x = bullet_x
            bullet.get_rect().y = bullet_y
    #Enchanted Blitting
    enchanted.update((player.get_rect().x, player.get_rect().y + 30))
    enchanted.draw(time, display, scroll)
    #Player Blitting
    if inventory[inven_slot] == "p" or inventory[inven_slot] == "s" or inventory[inven_slot] == "r":
        player.move(tile_rects, time, dt, display, scroll, True, inventory_items[str(inven_slot)].facing_direction(), inventory_items[str(inven_slot)])
    else:
        player.move(tile_rects, time, dt, display, scroll, False, yeagle.facing_direction())
    player.draw(display, scroll)
    #Blitting Items After Blitting The Player
    blit_grass(grasses, display, scroll, player)
    #Sparks Blitting
    for s in sparks:
        s.move(dt)
        s.draw(display)
    #Smoke Blitting
    for s in smokes:
        s.draw(display, scroll,time)
    #Mouse Blitting
    pygame.draw.circle(display,(200,0,0), (mpos[0]//2, mpos[1]//2), 4)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                #Normal Click To Shoot
                #yeagle.shoot((player_x - scroll[0], player_y - scroll[1]), bullet_img.get_width(), bullet_img.get_height(), angle)
                #Hold To Fire
                if inventory[inven_slot] == "s":
                    smg_spray = True
                if inventory[inven_slot] == "p" or inventory[inven_slot] == "r":
                    inventory_items[str(inven_slot)].shoot((player_x - scroll[0], player_y - scroll[1]), bullet_img.get_width(), bullet_img.get_height(), angle, time)
            if event.button == 3:
                if inventory[inven_slot] == "p":
                    inventory[inven_slot] = ""
                    item_dict["p"][2] = -2
                    pistols.append(inventory_items[str(inven_slot)])
                    inventory_items[str(inven_slot)] = None
                if inventory[inven_slot] == "s":
                    inventory[inven_slot] = ""
                    item_dict["s"][2] = -2
                    smgs.append(inventory_items[str(inven_slot)])
                    inventory_items[str(inven_slot)] = None
                if inventory[inven_slot] == "r":
                    inventory[inven_slot] = ""
                    item_dict["r"][2] = -2
                    rockets.append(inventory_items[str(inven_slot)])
                    inventory_items[str(inven_slot)] = None
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                smg_spray = False
    #Background Particles
    bg_particle_effect.recursive_call(time, display, scroll, dt)
    surf = pygame.transform.scale(display, (screen_w, screen_h))
    window.blit(surf, (0, 0))
    pygame.display.flip()