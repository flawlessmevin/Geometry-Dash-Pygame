import pygame

class Player:
    def __init__(self, x, y, image_path="assets/images/sprite.png"):
        self.x = x  # Начальная позиция по оси X
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

    def apply_gravity(self):

        self.velocity_y += 1
        self.y += self.velocity_y


        if self.y > 450 - self.height:
            self.y = 450 - self.height
            self.velocity_y = 0
            self.is_jumping = False

    def draw(self, screen):

        screen.blit(self.image, (self.x, self.y))

