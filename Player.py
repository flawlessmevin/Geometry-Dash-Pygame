import pygame

class Player:
    def __init__(self, x, y, image_path="assets/images/sprite.png"):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.velocity_y = 0
        self.is_jumping = False

        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

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
                    self.y = obj["rect"].top - self.height
                    self.is_jumping = False

        if self.y > 450 - self.height:
            self.y = 450 - self.height
            self.velocity_y = 0
            self.is_jumping = False

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)