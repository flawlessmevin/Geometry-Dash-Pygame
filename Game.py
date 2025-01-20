import pygame
from Player import Player
from Levels import Level

class Game:
    def __init__(self):
        pygame.init()

        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Geometry Dash Clone")

        self.clock = pygame.time.Clock()

        self.running = True

        self.background_image = pygame.image.load("assets/images/background.png")
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))

        self.player = Player(100, 450)
        self.level = Level("assets/levels.txt")

    def draw_background(self):
        self.screen.blit(self.background_image, (0, 0))

    def draw_ground(self):
        ground_color = (75, 0, 130)
        ground_height = 149
        pygame.draw.rect(self.screen, ground_color, (0, self.screen_height - ground_height, self.screen_width, ground_height))

        border_color = (255, 255, 255)
        border_height = 1
        pygame.draw.rect(self.screen, border_color, (0, self.screen_height - ground_height - border_height, self.screen_width, border_height))

    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.player.jump()

            self.player.apply_gravity()
            self.level.move_level()

            self.draw_background()
            self.draw_ground()
            self.level.draw(self.screen)
            self.player.draw(self.screen)

            pygame.display.update()

            self.clock.tick(60)

        pygame.quit()
