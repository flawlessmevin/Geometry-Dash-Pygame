from Settings import *
import random
import pygame


class Level:
    def __init__(self):
        self.level_patterns_file = LEVEL_PATTERNS
        self.current_frame = 0
        self.frame_counter = 0
        self.frame_delay = 5
        self.eliminated_objects = 0
        self.collided_objects = []
        self.level_grid = []
        self.generate_level()


        self.portal_image = pygame.transform.scale(pygame.image.load(PORTAL_IMAGE), (TILE_SIZE * 4, TILE_SIZE * 4))
        self.cube_image = pygame.transform.scale(pygame.image.load(CUBE_IMAGE), (TILE_SIZE, TILE_SIZE))
        self.triangle_image = pygame.transform.scale(pygame.image.load(TRIANGLE_IMAGE), (TILE_SIZE, TILE_SIZE))
        self.coin_images = [
            pygame.transform.rotozoom(
                pygame.image.load(f"assets/images/coin/Gold_{i}.png"),
                0,
                0.05
            )
            for i in range(1, 10)
        ]

        self.offset = 0
        self.explosion_sound = pygame.mixer.Sound("assets/sounds/explosion_sound.wav")

    def move_level(self):
        self.offset += 5
        for obj in self.collided_objects:
            obj["rect"].x -= 5

    def generate_level(self):
        with open(self.level_patterns_file, "r") as file:
            lines = file.readlines()
        patterns = [line.split(":")[1].strip() for line in lines if "Pattern" in line]

        level = ""
        for i in range(LEVEL_LENGTH // 5):
            level += random.choice(patterns)

        level = list(level)
        for i in range(len(level)):
            if level[i] == "." and random.random() < 0.05:
                level[i] = "*"

        level = "".join(level)
        #level = ".........#*#...*..#####....*#####*############################################################"
        level = ".........." + level[:LEVEL_LENGTH - 15] + ".........@"
        self.level_grid = [level]
        print(level)
        print(self.level_grid)

        self.collided_objects = []
        for row_idx, row in enumerate(self.level_grid):
            for col_idx, symbol in enumerate(row):
                x = col_idx * TILE_SIZE
                y = SCREEN_HEIGHT - (SCREEN_HEIGHT / 4) - TILE_SIZE
                print(symbol)

                if symbol == "@":
                    rect = pygame.Rect(x, y - 150, TILE_SIZE * 4, TILE_SIZE * 4)
                elif symbol == "*":

                    rect = pygame.Rect(x + TILE_SIZE / 4, y + TILE_SIZE / 4, TILE_SIZE // 2, TILE_SIZE // 2)
                else:
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

                if symbol in ["#", "^", "@", "*"]:
                    self.collided_objects.append({"rect": rect, "type": symbol})

    def eliminate_object(self, obj):
        self.explosion_sound.stop()
        self.collided_objects.remove(obj)
        self.explosion_sound.play()
        self.eliminated_objects += 1

    def draw(self, screen):


        for obj in self.collided_objects:
            rect = obj["rect"]
            obj_type = obj["type"]

            if obj_type == "#":
                screen.blit(self.cube_image, (rect.x, rect.y))
            elif obj_type == "^":
                screen.blit(self.triangle_image, (rect.x, rect.y))
            elif obj_type == "@":
                screen.blit(self.portal_image, (rect.x, rect.y))
            elif obj_type == "*":
                coin_image = self.coin_images[self.current_frame]
                screen.blit(coin_image, (rect.x, rect.y))

        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.coin_images)






    def get_progress(self):
        progress = (self.offset / (LEVEL_LENGTH * TILE_SIZE)) * 100
        return min(progress, 100)

    def draw_progress_bar(self, screen):
        progress = self.get_progress()
        bar_width = screen.get_width() * 0.8
        bar_height = 30

        pygame.draw.rect(screen, (50, 50, 50), (SCREEN_WIDTH * 0.1, 10, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (SCREEN_WIDTH * 0.1, 10, (bar_width * progress) / 100, bar_height))

        font = pygame.font.Font(FONT, 36)
        text = font.render(f"{int(progress)}", True, (255, 255, 255))

        text_x = SCREEN_WIDTH * 0.1 + bar_width / 2 - text.get_width() / 2
        text_y = 10 + (bar_height - text.get_height()) / 2
        screen.blit(text, (text_x, text_y))
