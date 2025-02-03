

import pygame
from Settings import *
import threading

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

    def enable_bonus(self):
        self.bonus = True
        self.bonus_time = pygame.time.get_ticks() + 3000
        threading.Timer(3, self.disable_bonus).start()

    def disable_bonus(self):
        self.bonus_time = 0
        self.bonus = False




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
                    self.image = pygame.transform.scale(self.images[0], (TILE_SIZE, TILE_SIZE))


        if self.y > SCREEN_HEIGHT - (SCREEN_HEIGHT/ 4) - TILE_SIZE:
            self.y = SCREEN_HEIGHT - (SCREEN_HEIGHT/ 4) - TILE_SIZE
            self.velocity_y = 0
            self.is_jumping = False
            self.image = pygame.transform.scale(self.images[0], (TILE_SIZE, TILE_SIZE))





    def draw(self, screen):

        screen.blit(self.image, (self.x, self.y))

    def draw_bonus_timer(self, screen):
        font = pygame.font.Font(pygame.font.get_default_font(), 50)
        #font = pygame.font.Font(FONT, 50)
        if self.bonus:
            remaining_time_ms = max(0, self.bonus_time - pygame.time.get_ticks())
            seconds = remaining_time_ms // 1000
            milliseconds = remaining_time_ms % 1000


            time_str = f"{seconds}.{milliseconds // 10:02d}"
            text = font.render(time_str, True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)