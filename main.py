#TODO -> Good Level Design
#TODO -> Songs Music
#TODO -> Death for player 

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
import Assets.Scripts.bullet as darts
import Assets.Scripts.shield as shield
import Assets.Scripts.water as water
import Assets.Scripts.fab as fab
import Assets.Scripts.eggs as egg
import Assets.Scripts.chicken as chicken
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
            pygame.draw.rect(display, (242,121,37), pygame.rect.Rect(left, 275, 20, 20), border_radius=5)
        draw_text(str(x+1), font, (255,255,255), left + 9, 294, display)
        pygame.draw.rect(display, (0,0,0), pygame.rect.Rect(left + 2, 275 + 2.5, 20 - 2.5, 20 - 2.5), border_radius=4)
        if item_dict.get(inventory[x]) != None:
            if item_dict[inventory[x]][0] == "Pistol":
                display.blit(item_dict[inventory[x]][1], (left + 3, 275 + 3.5))
            if item_dict[inventory[x]][0] == "SMG":
                display.blit(item_dict[inventory[x]][1], (left + 3, 275 + 3.5))
            if item_dict[inventory[x]][0] == "Rocket":
                display.blit(item_dict[inventory[x]][1], (left + 3, 275 + 3.5))
            if item_dict[inventory[x]][0] == "Shield":
                display.blit(item_dict[inventory[x]][1], (left + 3, 275 + 3.5))
            if item_dict[inventory[x]][0] == "Fab":
                display.blit(item_dict[inventory[x]][1], (left + 3, 275 + 3.5))
        left += 25

def blit_left_inventory(display, inventory, inven_slot, item_dict, inventory_items, font):
    left = 10
    pygame.draw.rect(display, (0,0,0), pygame.rect.Rect(0, 271, 110 , 40))
    pygame.draw.polygon(display, (0,0,0), [[110 - 6,270 + 2.5], [110 -6,300], [130 - 9,300]], 15)
    pygame.draw.line(display, (242,121,37), (left - 10, 270), (110, 270))
    pygame.draw.line(display, (242,121,37), (110, 270), (130 , 300))
    if inventory[inven_slot] == "p" or inventory[inven_slot] == "r" or inventory[inven_slot] == "s" :
        display.blit(item_dict[inventory[inven_slot]][3], (0, 275))
        flip = item_dict[inventory[inven_slot]][4].copy()
        if inventory[inven_slot] == "s":
            flip = pygame.transform.scale(flip, (flip.get_width()*2, flip.get_height()*2))
        else:
            flip = pygame.transform.scale(flip, (flip.get_width()*1.2, flip.get_height()*1.2))
        flip = pygame.transform.rotate(flip, 90)
        display.blit(flip, (50, 275))
        draw_text(str(inventory_items[str(inven_slot)].get_bullet_count()), font, (255,255,255), 70, 265, display )
    if inventory[inven_slot] == "l":
        display.blit(item_dict[inventory[inven_slot]][3], (0, 275))
        inventory_items[str(inven_slot)].draw_health_bar(display, 50, 290)
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
def main(map_loc, player_life, eggs_dropped):
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
    player_img = pygame.transform.scale(player_img, (player_img.get_width() * 3, player_img.get_height() * 3))
    player_img.set_colorkey((0,0,0))
    player_idle_img = pygame.image.load("./Assets/Sprites/player_idle.png").convert_alpha()
    player_run_img = pygame.image.load("./Assets/Sprites/player_run.png").convert_alpha()
    player_land_img_copy = pygame.image.load("./Assets/Sprites/player_land.png").convert_alpha()
    player_land_img = player_land_img_copy.copy()
    player_land_img = pygame.transform.scale(player_land_img_copy, (player_land_img_copy.get_width() * 1.2, player_land_img_copy.get_height() * 1.27))
    player_land_img.set_colorkey((0,0,0))
    player_load_img = pygame.image.load("./Assets/Sprites/player.png").convert_alpha()
    player_load_img = pygame.transform.scale(player_load_img, (player_load_img.get_width()*3, player_load_img.get_height()*3))
    player_load_img.set_colorkey((0,0,0))
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
    shield_img = pygame.image.load("./Assets/Entities/shield.png").convert_alpha()
    shield_img = pygame.transform.scale(shield_img, (shield_img.get_width() * 2.5, shield_img.get_height() * 3))
    shield_img.set_colorkey((0,0,0))
    fab_img = pygame.image.load("./Assets/Entities/fab.png").convert_alpha()
    fab_img = pygame.transform.scale(fab_img, (fab_img.get_width()*0.75, fab_img.get_height()*0.75))
    fab_img.set_colorkey((0,0,0))
    smg_bullet_img = pygame.image.load("./Assets/Entities/smg_bullet.png").convert_alpha()
    pistol_logo_img = pistol_img.copy()
    pistol_logo_img = pygame.transform.scale(pistol_logo_img, (pistol_logo_img.get_width()//2, pistol_img.get_height()//2))
    pistol_logo_img = pygame.transform.rotate(pistol_logo_img, 45)
    aim_point_img = pygame.image.load("./Assets/Entities/aim_point.png").convert_alpha()
    aim_point_img.set_colorkey((255,255,255))
    smg_logo_img = smg_img.copy()
    smg_logo_img = pygame.transform.scale(smg_logo_img, (smg_logo_img.get_width()//2, smg_logo_img.get_height()//2))
    smg_logo_img = pygame.transform.rotate(smg_logo_img, 45)
    fab_logo_img = pygame.image.load("./Assets/Entities/fab.png").convert_alpha()
    fab_logo_img = pygame.transform.scale(fab_logo_img, (fab_logo_img.get_width()//2, fab_logo_img.get_height()//2))
    fab_logo_img = pygame.transform.rotate(fab_logo_img, 45)
    rocket_logo_img = pygame.image.load("./Assets/Entities/rocket.png").convert_alpha()
    rocket_logo_img = pygame.transform.scale(rocket_logo_img, (rocket_logo_img.get_width()//1.5, rocket_logo_img.get_height()//1.5))
    rocket_logo_img = pygame.transform.rotate(rocket_logo_img, 45)
    shield_logo_img = pygame.image.load("./Assets/Entities/shield.png").convert_alpha()
    shield_logo_img = pygame.transform.scale(shield_logo_img, (shield_logo_img.get_width() * 1, shield_logo_img.get_height() * 1))
    shield_logo_img = pygame.transform.rotate(shield_logo_img, 45)
    chicken_idle_spritesheet = pygame.image.load("./Assets/Sprites/chicken_idle.png").convert_alpha()
    chicken_img = pygame.image.load("./Assets/Sprites/chicken.png").convert_alpha()
    chicken_img.set_colorkey((0,0,0))
    player_head_img = pygame.image.load("./Assets/Sprites/player_head.png").convert_alpha()
    player_head_img.set_colorkey((0,0,0))
    #Enemy animations
    enemy_costume = {'1' : [[], []], '2' : [[], []], '3' : [[], []], '4' : [[], []]}
    for x in range(4):
        url_idle = "./Assets/Sprites/enemy" + str(x+1) + "_idle.png"
        url_run = "./Assets/Sprites/enemy" + str(x + 1) + "_run.png"
        idle_spritesheet = pygame.image.load(url_idle).convert_alpha()
        run_spritesheet = pygame.image.load(url_run).convert_alpha()
        for y in range(4):
            enemy_costume[str(x+1)][0].append(get_image(idle_spritesheet, y, 15, 20, 1.8, (0,0,0)))
            enemy_costume[str(x+1)][1].append(get_image(run_spritesheet, y, 15, 20, 1.8, (0,0,0)))
    #Eggs
    egg_images = []
    for x in range(4):
        url = "./Assets/Entities/egg" + str(x+1) + ".png"
        img = pygame.image.load(url).convert_alpha()
        img.set_colorkey((0,0,0))
        egg_images.append(img)
    #Grass
    grasses = []
    grass_loc = []
    grass_spawn = True
    grass_last_update = 0
    grass_cooldown = 50
    #Map
    map = f.Map("./Assets/Maps/" + map_loc,tiles,tree_img)
    #Player settings
    player_idle_animation = []
    player_x = 0
    player_spawn = True
    player_y = 0
    player_run_animation = []
    for x in range(4):
        player_idle_animation.append(get_image(player_idle_img, x, 23, 37, 1.2, (0,0,0)))
    for x in range(4):
        player_run_animation.append(get_image(player_run_img, x, 23, 37, 1.2, (0,0,0)))
    #player = f.Player(30,30,player_idle_animation[0].get_width(),player_idle_animation[0].get_height(), player_img, player_idle_animation, player_run_animation, player_land_img)
    #Random Variables
    true_scroll = [0,0]
    scroll = [0,0]
    last_time = t.time()
    #Mouse Settings
    pygame.mouse.set_visible(False)
    #Fonts
    inven_font = pygame.font.Font("./Assets/Fonts/jayce.ttf", 5)
    pick_up_font = pygame.font.Font("./Assets/Fonts/jayce.ttf", 15)
    left_inven_font = pygame.font.Font("./Assets/Fonts/jayce.ttf", 30)
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
    item_dict = {"p" : ["Pistol", pistol_logo_img, -2, pistol_img, bullet_img], "s" : ["SMG", smg_logo_img, -2, smg_img, smg_bullet_img], "r" : ["Rocket", rocket_logo_img, -2, rocket_img, rocket_ammo_img], "l" : ["Shield", shield_logo_img, -2, shield_img], "f" : ["Fab", fab_logo_img, -2, fab_img]}
    #Enemy
    enemies = []
    enemy_spawn = True
    enemy_angle = 0
    enemy_bullets = []
    enemy_locs = []
    enemy_count = 0
    #Shield
    shields = []
    shield_spawn = True
    #Water
    waters = []
    water_spawn = True
    #Fab
    fabs = []
    fab_spawn = True
    #Eggs
    if eggs_dropped != []:
        eggs = eggs_dropped
        egg_spawn = False
    else:
        egg_spawn = True
        eggs = []
    collected_eggs = []
    #Chickens 
    chickens = []
    chicken_last_update = 0
    chicken_cooldown = 500
    chciken_idle_animation = []
    for x in range(4):
        chciken_idle_animation.append(get_image(chicken_idle_spritesheet, x, 12, 12, 2, (0,0,0)))
    #Speech
    speech = ["I have finally chosen my Champion", "You are No Longer A RABBIT", "              You are my TROBBIT", "              You are my TROBBIT", "Retrieve my EGGS from the humans", "They PAINT it, EAT it, OMELET it", "          You are the chosen one", "          You are the chosen one"]
    speech_last_update = 0
    speech_cooldown = 2200
    current_in_speech = 0
    frog_check = True
    if map_loc == "load.txt":
        frog_check = False
    #Death 
    death_cooldown = 1000
    death_last_update = 0
    lives = 3
    life_blit_left = 400
    #Main Game Loop
    while run:
        clock.tick(60)
        key = pygame.key.get_pressed()
        dt = t.time() - last_time
        dt *= 60
        last_time = t.time()
        time = pygame.time.get_ticks()
        if map_loc == "load.txt":
            display.fill((157,225,255))
            points = [[0,0], [500, 0], [250,200]]
            pygame.draw.polygon(display, (255,206,14), points )
            if time - chicken_last_update > chicken_cooldown:
                chicken_last_update = time
                random_choice = random.randint(0,1)
                if random_choice == 0:
                    chickens.append(chicken.Chicken([random.randint(-500,1000)//2, random.randint(-120,-60)//2], chciken_idle_animation[0].get_width(), chciken_idle_animation[1].get_height(), chciken_idle_animation, True ))
                else:
                    chickens.append(chicken.Chicken([random.randint(-500,1000)//2, random.randint(-120,-60)//2], chciken_idle_animation[0].get_width(), chciken_idle_animation[1].get_height(), chciken_idle_animation, False ))
        else:
            display.fill((157,225,255))
        #VFX
        for glow_effect in glow_effects:
            glow_effect.update(time, display, scroll)
        bg.recursive_call(display)
        #Mouse Settings 
        mpos = pygame.mouse.get_pos()
        #Blitting the Map
        tile_rects, grass_loc, pistol_locs, smg_locs, rocket_locs, menemy_locs, qenemy_locs, shield_locs, water_locs, fab_locs, egg_locs, player_loc  = map.blit_map(display, scroll)
        #Calculating Scroll
        if player_spawn:
            if map_loc == "load.txt":
                for loc in player_loc:
                    player = f.Player(loc[0],loc[1],player_img.get_width(),player_img.get_height(), player_img, player_idle_animation, player_run_animation, player_land_img)
            else:
                for loc in player_loc:
                    player = f.Player(loc[0],loc[1],player_idle_animation[0].get_width(),player_idle_animation[0].get_height(), player_img, player_idle_animation, player_run_animation, player_land_img)
            if player_life != -2:
                player.life = player_life
            player_spawn = False
        if map_loc == "load.txt":
            true_scroll[0] += (player.get_rect().x - true_scroll[0] - 222) 
        else:
            true_scroll[0] += (player.get_rect().x - true_scroll[0] - 262) 
        true_scroll[1] += (player.get_rect().y - true_scroll[1] - 200) 
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])
        #Creating Items
        if egg_spawn:
            for loc in egg_locs:
                random_number = random.randint(0,3)
                eggs.append(egg.Eggs(loc, egg_images[0].get_width(), egg_images[0].get_height(), egg_images[random_number], random_number))
            egg_spawn = False
        if fab_spawn:
            for loc in fab_locs:
                fabs.append(fab.Fab(loc, fab_img.get_width(), fab_img.get_height(), fab_img))
            fab_spawn = False
        if shield_spawn:
            for loc in shield_locs:
                shields.append(shield.Shield(loc, shield_img.get_width()//1.5, shield_img.get_height(), shield_img))
            shield_spawn = False
        if water_spawn:
            for loc in water_locs:
                waters.append(water.Water(loc[0], loc[1], 32, 32 * 2 - 5, 3))
            water_spawn = False
        if grass_spawn:
            for loc in grass_loc:
                x_pos = loc[0]
                while x_pos < loc[0] + 32:
                    x_pos += 2.5
                    grasses.append(g.grass([x_pos, loc[1]+14], 2, 18))
            grass_spawn = False
        if enemy_spawn:           
            for loc in menemy_locs:
                choice = random.randint(1,3)
                cooldown = [0,0]
                move = True
                if choice == 1:
                    gun = pistol.Pistol(loc, pistol_img.get_width(), pistol_img.get_height(), pistol_img, bullet_img)
                    cooldown = [1000, 2000]
                elif choice == 2:
                    gun = smg.SMG(loc, smg_img.get_width(), smg_img.get_height(), smg_img, smg_bullet_img)
                    cooldown = [100, 300]
                else:
                    gun = rocket.Rocket(loc,rocket_img.get_width(), rocket_img.get_height(), rocketb_img, rocket_img, rocket_ammo_img)
                    cooldown = [1000, 2000]
                enemies.append(enemy.Enemy(loc, enemy_costume["1"][0][0].get_width(), enemy_costume["1"][0][0].get_height(), random.randint(2,7), random.randint(cooldown[0],cooldown[1]), gun, enemy_costume, str(random.randint(1,4)), move ))
            for loc in qenemy_locs:
                choice = random.randint(1,3)
                cooldown = [0,0]
                move = False
                if choice == 1:
                    gun = pistol.Pistol(loc, pistol_img.get_width(), pistol_img.get_height(), pistol_img, bullet_img, 100)
                    cooldown = [1000, 2000]
                elif choice == 2:
                    gun = smg.SMG(loc, smg_img.get_width(), smg_img.get_height(), smg_img, smg_bullet_img)
                    cooldown = [100, 300]
                else:
                    gun = rocket.Rocket(loc,rocket_img.get_width(), rocket_img.get_height(), rocketb_img, rocket_img, rocket_ammo_img, 5)
                    cooldown = [1000, 2000]
                enemies.append(enemy.Enemy(loc, enemy_costume["1"][0][0].get_width(), enemy_costume["1"][0][0].get_height(), random.randint(2,7), random.randint(cooldown[0],cooldown[1]), gun, enemy_costume, str(random.randint(1,4)), move ))
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
        for w in waters:
            w.chain_call(display, scroll, player.get_rect(), time)
        #Checking for player death
        if player.alive:
            if player.health <= 0:
                player.alive = False
                for x in range(40):
                    sparks.append(spark.Spark([player.get_rect().x - scroll[0] ,player.get_rect().y - scroll[1] ], math.radians(random.randint(0,360)), random.randint(4,7), (255,127,39), 2, 1))
                death_last_update = time
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
        #Drawing Eggs
        for position, p in sorted(enumerate(eggs) ,reverse=True):
            if player.alive:
                if p.get_rect().colliderect(player.get_rect()):
                    if p.get_whoami() == 0:
                        color = (255,242,0)
                    elif p.get_whoami() == 1:
                        color = (109, 49, 110)
                    elif p.get_whoami() == 2:
                        color = (240, 134, 80)
                    else:
                        color = (255,255,255)
                    for x in range(23):
                        sparks.append(spark.Spark([p.get_rect().x - scroll[0] , p.get_rect().y - scroll[1]], math.radians(random.randint(0,360)), random.randint(2,5), color, 2, 2))
                    collected_eggs.append(p)
                    eggs.pop(position)
            p.draw(display, scroll)
            p.update(tile_rects)
        #Drawing chickens
        for position, p in sorted(enumerate(chickens), reverse=True):
            p.draw(display, scroll)
            p.update(tile_rects, time)
            if p.get_rect().y > 500:
                chickens.pop(position)
        #Drawing enemies
        if player.alive:
            for position, e in sorted(enumerate(enemies), reverse=True):
                enemy_angle = math.atan2(( (e.get_rect().y - scroll[1]) - (player.get_rect().y - scroll[1])) , ( (e.get_rect().x - scroll[0]) - (player.get_rect().x - scroll[0])))
                enemy_angle = math.pi - enemy_angle
                enemy_bullets = e.move(enemy_angle, time, tile_rects, scroll, (player.get_rect().x, player.get_rect().y))
                e.draw(display, scroll, enemy_angle)
                #Checking for collisions with player
                for bullet in enemy_bullets:
                    bullet_x = bullet.get_rect().x
                    bullet_y = bullet.get_rect().y
                    bullet.get_rect().x += scroll[0]
                    bullet.get_rect().y += scroll[1]
                    if inventory[inven_slot] == "l":
                        if inventory_items[str(inven_slot)].get_rect().colliderect(bullet.get_rect()):
                            bullet.alive = False
                            if bullet.get_gun() == "r":
                                inventory_items[str(inven_slot)].health -= 100
                            else:
                                inventory_items[str(inven_slot)].health -= 20
                            for x in range(30):
                                if bullet.get_gun() == "r":
                                    sparks.append(spark.Spark([bullet_x , bullet_y], math.radians(random.randint(0,360)), random.randint(7,14), (255,255,255), 2, 1))
                                else:
                                    smokes.append(f.Smoke((bullet_x + scroll[0], bullet_y + scroll[1])))
                    if bullet.get_rect().colliderect(player.get_rect()):
                        if bullet.alive:
                            if bullet.get_gun() == "r":
                                player.health -= 70
                            else:
                                player.health -= 10
                            scroll[0] += random.randint(-20,20)
                            scroll[1] += random.randint(-20,20)
                            for x in range(30):
                                if bullet.get_gun() == "r":
                                    scroll[0] += random.randint(-50,50)
                                    scroll[1] += random.randint(-50, 50)
                                    sparks.append(spark.Spark([bullet_x , bullet_y], math.radians(random.randint(0,360)), random.randint(7,14), (255,103,20 ), 2, 1))
                                else:
                                    smokes.append(f.Smoke((bullet_x + scroll[0], bullet_y + scroll[1]), (120,0,0)))
                                #sparks.append(spark.Spark([bullet_x , bullet_y], math.radians(random.randint(0,360)), random.randint(2,7), (255,103,20), 0.5, 1))
                        bullet.alive = False
                    for tile in tile_rects:
                        if tile.colliderect(bullet.get_rect()):
                            bullet.alive = False
                            for x in range(30):
                                if bullet.get_gun() == "r":
                                    sparks.append(spark.Spark([bullet_x , bullet_y], math.radians(random.randint(0,360)), random.randint(7,14), (255,255,255), 2, 1))
                                else:
                                    smokes.append(f.Smoke((bullet_x + scroll[0], bullet_y + scroll[1])))
                    bullet.get_rect().x = bullet_x
                    bullet.get_rect().y = bullet_y
                for bullet in bullets:
                    bullet_x = bullet.get_rect().x
                    bullet_y = bullet.get_rect().y
                    bullet.get_rect().x += scroll[0]
                    bullet.get_rect().y += scroll[1]
                    if bullet.get_rect().colliderect(e.get_rect()):
                        if bullet.get_gun() == "r":
                            scroll[0] += random.randint(-50,50)
                            scroll[1] += random.randint(-50, 50)
                            e.health -= 110
                        if bullet.get_gun() == "p":
                            scroll[0] += random.randint(-20,20)
                            scroll[1] += random.randint(-20,20)
                            e.health -= 30
                        if bullet.get_gun() == "s":
                            scroll[0] += random.randint(-20,20)
                            scroll[1] += random.randint(-20,20)
                            e.health -= 10
                        for x in range(30):
                            if bullet.get_gun() == "r":
                                bullets.append(darts.Bullet((bullet_x, bullet_y), 30, 30, bullet_img, 0, "s", time, True))
                                sparks.append(spark.Spark([bullet_x , bullet_y], math.radians(random.randint(0,360)), random.randint(7,14), (255,103,20 ), 2, 1))
                            else:
                                #sparks.append(spark.Spark([bullet_x , bullet_y], math.radians(random.randint(0,360)), random.randint(2,7), (255,103,20), 0.5, 1))
                                smokes.append(f.Smoke((bullet_x + scroll[0], bullet_y + scroll[1]), (200, 0,  0)))
                        bullet.alive = False
                    bullet.get_rect().x = bullet_x
                    bullet.get_rect().y = bullet_y
                if e.health <= 0:
                    if e.get_gun() == "p":
                        e.gun.bullet_count = 20
                        pistols.append(e.gun)
                    if e.get_gun() == "r":
                        e.gun.bullet_count = 2
                        e.gun.bullet_in_gun = True
                        rockets.append(e.gun)
                    if e.get_gun() == "s":
                        e.gun.bullet_count = 50
                        smgs.append(e.gun)
                    e.destroy()
                    enemies.pop(position)
        else:
            for position, p in sorted(enumerate(collected_eggs), reverse=True):
                p.rect.x = player.get_rect().x + random.randint(-8,8)
                p.rect.y = player.get_rect().y
                eggs.append(p)
                collected_eggs.pop(position)
            if time - death_last_update > death_cooldown:
                if player.life < lives:
                    player.life += 1
                    return [3, player.life, eggs]
                else:
                    return [4]
            
        #Drawing Shields
        for position, p in sorted(enumerate(shields), reverse = True):
            if p.get_rect().colliderect(player.get_rect()):
                #pop up e
                draw_text("E",pick_up_font, (255,255,255), p.get_rect().x - scroll[0] + 16, p.get_rect().y - 16 - scroll[1], display )
                if key[pygame.K_e]:
                    pos = free_inventory_slot(inventory)
                    if pos != "full" and item_dict["l"][2] < 0:
                        inventory[pos] = "l"
                        item_dict["l"][2] = pos
                        inventory_items[str(pos)] = p
                        shields.pop(position)
            p.update(tile_rects)
            p.draw(display, scroll)
        #Drawing fabs
        for position, p in sorted(enumerate(fabs), reverse=True):
            if p.get_rect().colliderect(player.get_rect()):
                #pop up e
                draw_text("E",pick_up_font, (255,255,255), p.get_rect().x - scroll[0] + 16, p.get_rect().y - 16 - scroll[1], display )
                if key[pygame.K_e]:
                    pos = free_inventory_slot(inventory)
                    if pos != "full" and item_dict["f"][2] < 0:
                        inventory[pos] = "f"
                        item_dict["f"][2] = pos
                        inventory_items[str(pos)] = p
                        fabs.pop(position)
            p.draw(display, scroll)
            p.update(tile_rects, time, player)
        #Smg Spray Shoot
        if smg_spray:
            if time - smg_last_update > smg_cooldown:
                if inventory[inven_slot] == "s":
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
        if player.alive:
            if player.right_facing():
                player_x = player.get_rect().x + 22
                player_y = player.get_rect().y + 15
            else:
                player_x = player.get_rect().x - 1
                player_y = player.get_rect().y + 15
            #Angle Calculation
            angle = math.atan2(( mpos[1]//2 - (player_y - scroll[1])) , (mpos[0]//2 - (player.get_rect().x - scroll[0])))
            angle *= -1
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
                                bullets.append(darts.Bullet((bullet_x  + random.randint(-200, 260), bullet_y + random.randint(-200,200)), 30, 30, bullet_img, math.radians(random.randint(0,360)), "p", time, True))
                                sparks.append(spark.Spark([bullet_x , bullet_y], math.radians(random.randint(0,360)), random.randint(7,14), (255,255,255), 2, 1))
                            else:
                                smokes.append(f.Smoke((bullet_x + scroll[0], bullet_y + scroll[1])))

                    bullet.get_rect().x = bullet_x
                    bullet.get_rect().y = bullet_y
            #Enchanted Blitting
            enchanted.update((player.get_rect().x, player.get_rect().y + 30))
            if frog_check:
                if inven_slot != -1 and inventory[inven_slot] == "f":
                    if inven_slot != -1 or inventory_items.get(str(inven_slot)).get_use() == True:
                        enchanted.draw(time, display, scroll, (0,230,0))
                    else:
                        enchanted.draw(time, display, scroll)
                else:
                    enchanted.draw(time, display, scroll)
            #Player Blitting
            if not map_loc == "load.txt":
                if inven_slot != -1 and inventory[inven_slot] == "p" or inventory[inven_slot] == "s" or inventory[inven_slot] == "r":
                    player.move(tile_rects, time, dt, display, scroll, True, inventory_items[str(inven_slot)].facing_direction(), inventory_items[str(inven_slot)])
                elif inven_slot != -1 and inventory[inven_slot] == "l":
                    player.move(tile_rects, time, dt, display, scroll, False, inventory_items[str(inven_slot)].facing_direction(), inventory_items[str(inven_slot)], True)     
                elif inven_slot != -1 and inventory[inven_slot] == "f":
                    player.move(tile_rects, time, dt, display, scroll, False, inventory_items[str(inven_slot)].facing_direction(), inventory_items[str(inven_slot)])  
                else:
                    player.move(tile_rects, time, dt, display, scroll, False, yeagle.facing_direction())
            else:
                player.move(tile_rects, time, dt, display, scroll, False, yeagle.facing_direction(), can_move=False)
            if not map_loc == "load.txt":
                player.draw(display, scroll)
            else:
                if frog_check:
                    player.draw(display, scroll, player_img)
                else:
                    player.draw(display, scroll, player_load_img)
                if time - speech_last_update > speech_cooldown:
                    if current_in_speech < len(speech) - 1:
                        current_in_speech += 1
                    else:
                        return [0]
                    speech_last_update = time
                if speech[current_in_speech] == "              You are my TROBBIT":
                    frog_check = True
                draw_text(speech[current_in_speech], left_inven_font, (84,171,36), 20,140,display )
        #Blitting Items After Blitting The Player
        blit_grass(grasses, display, scroll, player)
        if inventory_items.get(str(inven_slot)) != None:
            if inventory[inven_slot] == "p" or inventory[inven_slot] == "s" or inventory[inven_slot] == "r":
                inventory_items[str(inven_slot)].draw(display, scroll, angle)
                bullets = inventory_items[str(inven_slot)].update(time, tile_rects)
            if inventory[inven_slot] == "l":
                inventory_items[str(inven_slot)].draw(display, scroll)
            if inventory[inven_slot] == "f":
                inventory_items[str(inven_slot)].draw(display, scroll)
                alive = inventory_items[str(inven_slot)].update(tile_rects, time, player)
                if not alive:
                    inventory[inven_slot] = ""
                    item_dict["f"][2] = -2
                    inventory_items[str(inven_slot)] = None
        #Sparks Blitting
        for s in sparks:
            s.move(dt)
            s.draw(display)
        #Smoke Blitting
        for s in smokes:
            s.draw(display, scroll,time)
        if map_loc == "load.txt":
            display.blit(chicken_img, (150, 0))
            for x in range(20):
                smokes.append(f.Smoke((random.randint(230,260) + scroll[0], random.randint(0,100) + scroll[1]), (234,63,247)))
        #Mouse Blitting
        #pygame.draw.circle(display,(200,0,0), (mpos[0]//2, mpos[1]//2), 4)
        display.blit(aim_point_img, (mpos[0]//2 + aim_point_img.get_width()//2 - 15, mpos[1]//2 - 15 + aim_point_img.get_height()//2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return [2]
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    #Normal Click To Shoot
                    #yeagle.shoot((player_x - scroll[0], player_y - scroll[1]), bullet_img.get_width(), bullet_img.get_height(), angle)
                    #Hold To Fire
                    if inventory[inven_slot] == "s":
                        smg_spray = True
                    if inventory[inven_slot] == "p" or inventory[inven_slot] == "r":
                        inventory_items[str(inven_slot)].shoot((player_x - scroll[0], player_y - scroll[1]), bullet_img.get_width(), bullet_img.get_height(), angle, time)
                    if inventory[inven_slot] == "f":
                        inventory_items[str(inven_slot)].use()
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
                    if inventory[inven_slot] == "l":
                        inventory[inven_slot] = ""
                        item_dict["l"][2] = -2
                        shields.append(inventory_items[str(inven_slot)])
                        inventory_items[str(inven_slot)] = None
                    if inventory[inven_slot] == "f":
                        inventory[inven_slot] = ""
                        item_dict["f"][2] = -2
                        fabs.append(inventory_items[str(inven_slot)])
                        inventory_items[str(inven_slot)] = None
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    smg_spray = False
        #Background Particles
        bg_particle_effect.recursive_call(time, display, scroll, dt)
        left = life_blit_left
        for x in range(lives - player.life):
            display.blit(player_head_img, (left, 0))
            left += 40
        display.blit(egg_images[2], (0, 30))
        text = str(len(collected_eggs)) + "/" + str(len(eggs) + len(collected_eggs))
        draw_text(text, left_inven_font, (255,255,255), 22, 30, display)
        #Checking if won 
        if len(eggs) == 0 and map_loc != "load.txt":
            return [0]
        blit_inventory(display, inventory, inven_font, item_dict, inven_slot)
        blit_left_inventory(display, inventory, inven_slot, item_dict, inventory_items, left_inven_font )
        surf = pygame.transform.scale(display, (screen_w, screen_h))
        window.blit(surf, (0, 0))
        pygame.display.flip()

def game():
    #O -> success
    #1 -> Failure
    #2 -> Exit
    #levels = ["load.txt", "map.txt"]
    
    run = True
    glow_effects = []
    bg1 = backg.background()
    clock = pygame.time.Clock()
    start_collide = False
    trial_collide = False
    start_rect = pygame.rect.Rect(150, 100, 200, 50)
    practice_rect = pygame.rect.Rect(150, 200, 200, 50)
    main_font = pygame.font.Font("./Assets/Fonts/jayce.ttf", 50)
    main_screen_img = pygame.image.load("./Assets/Entities/main_screen.png").convert_alpha()
    main_screen_img = pygame.transform.scale(main_screen_img, (main_screen_img.get_width()//4, main_screen_img.get_height()//4))
    for x in range(150):
        glow_effects.append(f.Glow((random.randint(-1000, 3000), random.randint(-100,700))))
    while run:
        clock.tick(60)
        time = pygame.time.get_ticks()
        pygame.mouse.set_visible(True)
        mpos = list(pygame.mouse.get_pos())
        mpos[0] = mpos[0]//2
        mpos[1] = mpos[1]//2
        start_collide = False
        trial_collide = False
        display.fill((157,225,255))
        for glow_effect in glow_effects:
            glow_effect.update(time, display, [0,0])
        bg1.recursive_call(display)
        display.blit(main_screen_img, (180,0))
        pygame.draw.rect(display, (255, 174, 201), start_rect, border_radius=50)
        pygame.draw.rect(display, (0, 0, 230), practice_rect, border_radius=50)
        draw_text("START", main_font, (0,0,0), 185, 95, display)
        draw_text("TRIAL", main_font, (0,0,0), 195, 195, display)
        if start_rect.collidepoint(mpos):
            start_collide = True
        if practice_rect.collidepoint(mpos):
            trial_collide = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if start_collide:
                        returned = start()
                        if returned == 2:
                            run = False
                    if trial_collide:
                        print("Collided")
        surf = pygame.transform.scale(display, (screen_w, screen_h))
        window.blit(surf, (0, 0))
        pygame.display.flip()

def start():
    levels = ["level1.txt", "level2.txt"]
    current_level = 0
    player_life = -2
    eggs = []
    while current_level < len(levels):
        returned_list = main(levels[current_level], player_life, eggs)
        if returned_list[0] == 0:
            current_level += 1
        if returned_list[0] == 2:
            return 2
        if returned_list[0] == 3:
            player_life = returned_list[1]
            eggs = returned_list[2]
        if returned_list[0] == 4:
            return 

game()