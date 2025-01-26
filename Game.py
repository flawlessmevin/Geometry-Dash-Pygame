import pygame

import Settings
from Player import Player
from Levels import Level
from Settings import *

class Game:
    def __init__(self):
        self.level = None
        self.player = None
        self.running = None
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Geometry Dash beta))")
        self.game_status = 0 # 0-not started or started, 1 - win, 2 - lose
        self.clock = pygame.time.Clock()


        self.button_text = "START"

        pygame.mixer.music.load("assets/sounds/background_music.mp3")
        pygame.mixer.music.play(-1)
        self.death_sound = pygame.mixer.Sound("assets/sounds/death_sound.mp3")
        self.win_sound = pygame.mixer.Sound("assets/sounds/win_sound.wav")

        self.background_image = pygame.image.load("assets/images/background.png")
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))


        self.menu()

    def draw_background(self):
        self.screen.blit(self.background_image, (0, 0))

    def draw_ground(self):
        ground_color = (75, 0, 130)
        ground_height = SCREEN_HEIGHT / 4 -1
        pygame.draw.rect(self.screen, ground_color, (0, SCREEN_HEIGHT - ground_height, SCREEN_WIDTH, ground_height))
        border_color = (255, 255, 255)
        border_height = 1
        pygame.draw.rect(self.screen, border_color, (0, SCREEN_HEIGHT - ground_height - border_height, SCREEN_WIDTH, border_height))

    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.player.jump()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.player.jump()

            self.player.apply_gravity(self.level.collided_objects)
            self.level.move_level()
            self.draw_background()
            self.level.draw_progress_bar(self.screen)
            self.draw_ground()
            self.check_collisions()
            self.level.draw(self.screen)
            self.player.draw(self.screen)

            pygame.display.update()

            self.clock.tick(60)
        pygame.quit()

    def check_collisions(self):
        for obj in self.level.collided_objects:
            if obj["rect"].colliderect(self.player.get_rect()):
                if obj["type"] == "#":
                    if self.player.get_rect().colliderect(obj["rect"]):
                        if self.player.get_rect().right > obj["rect"].left and self.player.get_rect().left < obj["rect"].left:
                            self.game_status = 2
                            self.death_sound.play()
                            self.menu()

                elif obj["type"] == "^":
                    if self.player.get_rect().colliderect(obj["rect"]):
                        self.game_status = 2
                        self.death_sound.play()
                        self.menu()

                elif obj["type"] == "@":
                    if self.player.get_rect().colliderect(obj["rect"]):
                        self.win_sound.play()
                        self.game_status = 1
                        self.menu()

    def start_game(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.play(-1)
        self.win_sound.stop()
        self.player = Player(SCREEN_WIDTH/ 4, SCREEN_HEIGHT - (SCREEN_HEIGHT/ 4) - TILE_SIZE)
        self.level = Level()
        self.game_loop()

    def menu(self):
        if self.game_status != 0:
            self.button_text = "RESTART"
        self.draw_background()
        self.running = True
        pygame.mixer.music.stop()
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        font = pygame.font.Font("assets/fonts/ARCADECLASSIC.TTF", 72)
        if self.game_status == 1:
            text = font.render("YOU WIN", True, (255, 255, 255))
        elif self.game_status == 2:
            text = font.render("YOU   LOSE", True, (255, 255, 255))
        else:
            text = font.render("WE LCOME", True, (255, 255, 255))

        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))

        button_font = pygame.font.Font("assets/fonts/ARCADECLASSIC.TTF", 36)
        restart_button = self.create_buttons((SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2), self.button_text, button_font)
        exit_button = self.create_buttons((SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100), "Exit", button_font)

        while True:
            self.screen.blit(overlay, (0, 0))
            self.screen.blit(text, text_rect)
            self.screen.blit(*restart_button)
            self.screen.blit(*exit_button)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.win_sound.stop()
                    self.death_sound.stop()
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button[1].collidepoint(event.pos):
                        self.start_game()
                        return
                    if exit_button[1].collidepoint(event.pos):
                        pygame.quit()
                        exit()

    @staticmethod
    def create_buttons(position, text, font):
        button_surface = pygame.Surface((300, 50))
        button_surface.fill((75, 75, 75))

        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(150, 25))
        button_surface.blit(text_surface, text_rect)

        button_rect = button_surface.get_rect(topleft=position)

        return button_surface, button_rect



