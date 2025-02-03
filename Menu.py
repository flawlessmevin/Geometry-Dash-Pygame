import pygame
from Settings import *

class Menu:
    def __init__(self, game):
        self.game = game

    def show_menu(self):
        if self.game.game_status != 0:
            button_text = "RESTART"
        else:
            button_text = "START"

        self.game.draw_background()
        pygame.mixer.music.stop()
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        font = pygame.font.Font(FONT, 72)
        if self.game.game_status == 1:
            text = font.render("YOU WIN", True, (255, 255, 255))
        elif self.game.game_status == 2:
            text = font.render("YOU LOSE", True, (255, 255, 255))
        else:
            text = font.render("WELCOME", True, (255, 255, 255))

        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))

        button_font = pygame.font.Font(FONT, 36)
        restart_button = self.create_buttons((SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2), button_text, button_font)
        exit_button = self.create_buttons((SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100), "Exit", button_font)

        while True:
            self.game.screen.blit(overlay, (0, 0))
            self.game.screen.blit(text, text_rect)
            self.game.screen.blit(*restart_button)
            self.game.screen.blit(*exit_button)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.win_sound.stop()
                    self.game.death_sound.stop()
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button[1].collidepoint(event.pos):
                        self.game.start_game()
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
