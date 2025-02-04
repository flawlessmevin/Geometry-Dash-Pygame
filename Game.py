import pygame


from Player import Player
from Levels import Level
from Settings import *
from Menu import Menu

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

        self.menu = Menu(self)



        self.button_text = "START"

        pygame.mixer.music.load("assets/sounds/background_music.mp3")
        pygame.mixer.music.play(-1)
        self.death_sound = pygame.mixer.Sound("assets/sounds/death_sound.mp3")
        self.win_sound = pygame.mixer.Sound("assets/sounds/win_sound.wav")
        self.coin_sound = pygame.mixer.Sound("assets/sounds/coin_sound.wav")


        self.background_image = pygame.image.load("assets/images/background.png")
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))


        self.menu.show_menu(0, 0, 0)

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
            self.player.update()
            self.player.draw(self.screen)


            pygame.display.update()

            self.clock.tick(60)
        pygame.quit()

    def check_collisions(self):
        for obj in self.level.collided_objects:
            if obj["rect"].colliderect(self.player.get_rect()):
                if not self.player.bonus:
                    if obj["type"] == "#":
                        if self.player.get_rect().colliderect(obj["rect"]):
                            if self.player.get_rect().right > obj["rect"].left and self.player.get_rect().left < obj["rect"].left:
                                self.game_status = 2
                                self.death_sound.play()
                                self.menu.show_menu(self.player.bonus_collected, self.level.eliminated_objects, self.level.get_progress())

                    elif obj["type"] == "^":
                        if self.player.get_rect().colliderect(obj["rect"]):
                            self.game_status = 2
                            self.death_sound.play()
                            self.menu.show_menu(self.player.bonus_collected, self.level.eliminated_objects, self.level.get_progress())

                    elif obj["type"] == "@":
                        if self.player.get_rect().centerx >= obj["rect"].centerx:
                            self.win_sound.play()
                            self.game_status = 1
                            self.menu.show_menu(self.player.bonus_collected, self.level.eliminated_objects, self.level.get_progress())

                    elif obj["type"] == "*":
                        if self.player.get_rect().colliderect(obj["rect"]):
                            self.level.collided_objects.remove(obj)
                            self.coin_sound.play()
                            self.player.add_bonus_time(2000)

                else:
                    if obj["type"] == "*":
                        self.coin_sound.play()
                        self.level.collided_objects.remove(obj)
                        self.player.add_bonus_time(2000)
                    elif obj["type"] == "@":
                        if self.player.get_rect().centerx >= obj["rect"].centerx:
                            self.win_sound.play()
                            self.game_status = 1
                            self.menu.show_menu(self.player.bonus_collected, self.level.eliminated_objects, self.level.get_progress())
                    elif obj["type"] == "^" or obj["type"] == "#":
                        self.level.eliminate_object(obj)



    def start_game(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.play(-1)
        self.win_sound.stop()
        self.player = Player(SCREEN_WIDTH/ 4, SCREEN_HEIGHT - (SCREEN_HEIGHT/ 4) - TILE_SIZE)
        self.level = Level()
        self.running = True
        self.game_loop()




