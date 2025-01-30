import pygame
from Settings import *

class Player:
    def __init__(self, x, y, image_paths=PLAYER_IMAGES):
        self.x = x
        self.y = y
        self.velocity_y = 0
        self.is_jumping = False
        self.images = [pygame.image.load(path) for path in image_paths]
        self.image = pygame.transform.scale(self.images[0], (TILE_SIZE, TILE_SIZE))



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

    def get_rect(self):
        return pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)