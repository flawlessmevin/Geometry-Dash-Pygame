from Settings import *
import pygame

class BonusTimer:
    def __init__(self, player):
        self.bonus_end_time = 0
        self.player = player

    def add_time(self, duration):
        if self.player.bonus:
            self.bonus_end_time += duration
        else:
            self.bonus_end_time = pygame.time.get_ticks() + duration
            self.player.bonus = True

    def update(self):
        if self.player.bonus and pygame.time.get_ticks() >= self.bonus_end_time:
            self.player.bonus = False

    def draw_bonus_timer(self,screen):

        font = pygame.font.Font(FONT, 50)
        if self.player.bonus:
            remaining_time_ms = max(0, self.bonus_end_time - pygame.time.get_ticks())
            seconds = remaining_time_ms // 1000
            milliseconds = remaining_time_ms % 1000


            time_str = f"{seconds}.{milliseconds // 10:02d}"
            text = font.render(time_str, True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - SCREEN_HEIGHT // 6))
            screen.blit(text, text_rect)