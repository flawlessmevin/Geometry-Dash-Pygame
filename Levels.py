from Settings import *

import random


import pygame

class Level:


    SYMBOLS = {
        "#": "assets/images/cube.png",
        "^": "assets/images/triangle.png",
        "@": "assets/images/portal.png",
        "*": "assets/images/bonus_coin.png",
        ".": None
    }

    def __init__(self):
        self.file_path = "assets/level_patterns.txt"
        self.collided_objects = []
        self.level_grid = []

        self.generate_level()
        self.images = self.load_images()
        self.offset = 0
        self.explosion_sound = pygame.mixer.Sound("assets/sounds/explosion_sound.wav")



    def move_level(self):
        self.offset += 5

        for obj in self.collided_objects:
            obj["rect"].x -= 5



    def generate_level(self):
        with open(self.file_path, "r") as file:
            lines = file.readlines()
        patterns = [line.split(":")[1].strip() for line in lines if "Pattern" in line]

        level = ""

        for i in range(LEVEL_LENGTH // 5):
            level += random.choice(patterns)
        level = list(level)
        for i in range(len(level)):
            if level[i] == "." and random.random() < 0.1:
                level[i] = "*"
                print(i)
        level = "".join(level)
        level = "..............#####*#################################################################"
        #level = ".........." + level[:LEVEL_LENGTH - 15] + ".........@"



        self.level_grid = [level]

        self.collided_objects = []

        for row_idx, row in enumerate(self.level_grid):
            for col_idx, symbol in enumerate(row):
                if symbol in self.SYMBOLS and self.SYMBOLS[symbol] is not None:
                    x = col_idx * TILE_SIZE
                    y = SCREEN_HEIGHT - (SCREEN_HEIGHT/ 4) - TILE_SIZE
                    if symbol == "@":
                        rect = pygame.Rect(x, y - 150, TILE_SIZE * 4 , TILE_SIZE * 4)
                    elif symbol == "*":
                        rect = pygame.Rect(x + TILE_SIZE/4, y+TILE_SIZE/4, TILE_SIZE/2, TILE_SIZE/2)
                    else:
                        rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.collided_objects.append({"rect": rect, "type": symbol})


    def load_images(self):
        images = {}
        for symbol, path in self.SYMBOLS.items():
            if path:
                images[symbol] = pygame.image.load(path)
                if symbol == "@":
                    images[symbol] = pygame.transform.scale(images[symbol], (TILE_SIZE * 4, TILE_SIZE * 4))
                elif symbol == "*":
                    images[symbol] = pygame.transform.scale(images[symbol], (TILE_SIZE/2, TILE_SIZE/2))
                else:
                    images[symbol] = pygame.transform.scale(images[symbol], (TILE_SIZE, TILE_SIZE))
        return images

    def eliminate_object(self, obj):
        self.explosion_sound.stop()
        self.collided_objects.remove(obj)
        self.explosion_sound.play()





    def draw(self, screen):
        for obj in self.collided_objects:
            if obj["type"] in self.images:
                screen.blit(self.images[obj["type"]], (obj["rect"].x, obj["rect"].y))



    def get_progress(self):

        progress = (self.offset / (LEVEL_LENGTH * TILE_SIZE)) * 100
        progress = min(progress, 100)
        return progress

    def draw_progress_bar(self, screen):
        progress = self.get_progress()
        bar_width = screen.get_width() * 0.8
        bar_height = 30

        pygame.draw.rect(screen, (50, 50, 50), (SCREEN_WIDTH * 0.1, 10, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (SCREEN_WIDTH * 0.1, 10, (bar_width * progress) / 100, bar_height))

        font = pygame.font.Font("assets/fonts/ARCADECLASSIC.TTF", 36)
        text = font.render(f"{int(progress)}", True, (255, 255, 255))

        text_x = SCREEN_WIDTH * 0.1 + bar_width / 2 - text.get_width() / 2
        text_y = 10 + (bar_height - text.get_height()) / 2
        screen.blit(text, (text_x, text_y))