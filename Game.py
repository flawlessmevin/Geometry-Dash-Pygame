import pygame
from Player import Player
from Levels import Level

class Game:
    def __init__(self):
        pygame.init()

        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Geometry Dash beta))")

        self.game_won = False

        self.clock = pygame.time.Clock()

        self.running = True

        pygame.mixer.music.load("assets/sounds/background_music.mp3")

        pygame.mixer.music.play(-1)

        self.death_sound = pygame.mixer.Sound("assets/sounds/death_sound.mp3")


        self.win_sound = pygame.mixer.Sound("assets/sounds/win_sound.wav")
        self.win_sound.set_volume(1)

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
                            self.death_sound.play()
                            self.restart_game()
                elif obj["type"] == "^":
                    if self.player.get_rect().colliderect(obj["rect"]):
                        self.death_sound.play()
                        self.restart_game()

                elif obj["type"] == "@":
                    if self.player.get_rect().colliderect(obj["rect"]):
                        if not self.game_won:
                            self.win_game()





    def restart_game(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.play(-1)
        self.win_sound.stop()

        self.player = Player(100, 450)
        self.level = Level("assets/levels.txt")
        self.game_loop()






    def win_game(self):
        self.game_won = True
        pygame.mixer.music.stop()
        self.win_sound.play()

        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)

        font = pygame.font.Font("assets/fonts/ARCADECLASSIC.TTF", 72)
        text = font.render("YOU WIN", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 3))


        button_font = pygame.font.Font("assets/fonts/ARCADECLASSIC.TTF", 36)
        restart_button = self.create_buttons((self.screen_width // 2 - 150, self.screen_height // 2), "Restart",
                                            button_font)
        exit_button = self.create_buttons((self.screen_width // 2 - 150, self.screen_height // 2 + 100), "Exit",
                                         button_font)


        while True:
            self.screen.blit(overlay, (0, 0))
            self.screen.blit(text, text_rect)
            self.screen.blit(*restart_button)
            self.screen.blit(*exit_button)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button[1].collidepoint(event.pos):
                        self.restart_game()
                        return
                    if exit_button[1].collidepoint(event.pos):
                        pygame.quit()
                        exit()

    def create_buttons(self, position, text, font):
        button_surface = pygame.Surface((300, 50))
        button_surface.fill((75, 75, 75))

        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(150, 25))
        button_surface.blit(text_surface, text_rect)

        button_rect = button_surface.get_rect(topleft=position)

        return button_surface, button_rect



