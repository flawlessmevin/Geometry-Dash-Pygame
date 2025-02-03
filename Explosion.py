import pygame
from Settings import *

class Explosion:
    def __init__(self, x, y):
        self.frames = [pygame.image.load(f"assets/images/explosion/frame{i}.png") for i in range(0, 15)]
        self.current_frame = 0
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.frame_rate = 50
        self.last_frame_update = pygame.time.get_ticks()
        self.done = False

    def update(self):

        if pygame.time.get_ticks() - self.last_frame_update > self.frame_rate:
            self.current_frame += 1
            self.last_frame_update = pygame.time.get_ticks()
            if self.current_frame >= len(self.frames):
                self.done = True

    def draw(self, screen):
        if not self.done:

            screen.blit(self.frames[self.current_frame], (self.x, self.y))

    def get_rect(self):

        return self.rect