import pygame
from Settings import *
from BonusTimer import BonusTimer


class Player:
    def __init__(self, x, y, image_paths=PLAYER_IMAGES):
        self.x = x
        self.y = y
        self.velocity_y = 0
        self.is_jumping = False
        self.bonus = False
        self.bonus_time = 0
        self.images = [pygame.image.load(path) for path in image_paths]
        self.image = pygame.transform.scale(self.images[0], (TILE_SIZE, TILE_SIZE))
        self.bonus_timer = BonusTimer(self)
        self.bonus_collected = 0



    def jump(self):
        if not self.is_jumping:
            self.velocity_y = -15
            self.is_jumping = True
            self.image = pygame.transform.scale(self.images[1], (TILE_SIZE, TILE_SIZE))


    def apply_gravity(self, collided_objects):
        self.velocity_y += 1
        self.y += self.velocity_y

        for obj in collided_objects:
            if obj["type"] == "#":
                if obj["rect"].collidepoint(self.get_rect().centerx, self.get_rect().bottom):
                    self.velocity_y = 0
                    self.y = obj["rect"].top - TILE_SIZE
                    self.is_jumping = False



        if self.y > SCREEN_HEIGHT - (SCREEN_HEIGHT/ 4) - TILE_SIZE:
            self.y = SCREEN_HEIGHT - (SCREEN_HEIGHT/ 4) - TILE_SIZE
            self.velocity_y = 0
            self.is_jumping = False



    def add_bonus_time(self, duration):
        self.bonus_timer.add_time(duration)
        self.bonus_collected += 1


    def update(self):
        self.bonus_timer.update()
        if self.bonus:
            if self.is_jumping:
                self.image = pygame.transform.scale(self.images[3], (TILE_SIZE, TILE_SIZE))
            else:
                self.image = pygame.transform.scale(self.images[2], (TILE_SIZE, TILE_SIZE))

        else:
            if self.is_jumping:
                self.image = pygame.transform.scale(self.images[1], (TILE_SIZE, TILE_SIZE))
            else:
                self.image = pygame.transform.scale(self.images[0], (TILE_SIZE, TILE_SIZE))


    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        if self.bonus:
            self.bonus_timer.draw_bonus_timer(screen)


    def get_rect(self):
        return pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)