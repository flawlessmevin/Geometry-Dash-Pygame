import pygame
from Settings import *

class Player:
    def __init__(self, x, y, image_path="assets/images/sprite.png"):
        self.x = x
        self.y = y
        self.velocity_y = 0
        self.is_jumping = False
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = -15
            self.is_jumping = True

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

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)