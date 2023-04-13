import pygame

class Shield():
    def __init__(self, loc, width, height, img) -> None:
        self.rect = pygame.rect.Rect(loc[0], loc[1], width, height)
        self.display_x = 0
        self.display_y = 0
        self.movement = []
        self.collision_types = {}
        self.img = img
        self.facing_right = True
        self.health = 100
    
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
        self.collision_types = self.collision_checker(tiles)
    
    def draw_health_bar(self, display, x, y):
        x -= 25
        y -= 10
        ratio = self.health / 100
        pygame.draw.rect(display, (2,17,179), (x - 2, y - 2, 80  , 27//2))
        pygame.draw.rect(display, (255,0,0), (x, y, 76  , 25//2))
        pygame.draw.rect(display, (202,68,255), (x, y, 76 * ratio , 25//2))
    
    def draw(self, display, scroll):
        self.display_x = self.rect.x
        self.display_y = self.rect.y
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        if self.facing_right:
            display.blit(self.img, self.rect)
        else:
            flip = self.img.copy()
            flip = pygame.transform.flip(flip, True, False)
            display.blit(flip, self.rect)
        self.rect.x = self.display_x
        self.rect.y = self.display_y
    
    def facing_direction(self):
        return False
    
    def get_rect(self):
        return self.rect