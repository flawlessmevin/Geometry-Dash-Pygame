import pygame

class Level:
    TILE_SIZE = 50

    SYMBOLS = {
        "#": "assets/images/cube.png",
        "^": "assets/images/triangle.png",
        ".": None
    }

    def __init__(self, file_path):
        self.file_path = file_path
        self.collided_objects = []
        self.grid = []
        self.load_level()
        self.images = self.load_images()
        self.offset = 0

    def move_level(self):
        self.offset += 5

        for obj in self.collided_objects:
            obj["rect"].x -= 5

    def load_level(self):
        with open(self.file_path, "r") as file:
            lines = file.readlines()

        self.grid = [line.strip() for line in lines if line.strip() and not line.startswith("Level")]

        self.collided_objects = []

        for row_idx, row in enumerate(self.grid):
            for col_idx, symbol in enumerate(row):
                if symbol in self.SYMBOLS and self.SYMBOLS[symbol] is not None:

                    x = col_idx * self.TILE_SIZE
                    y = 450 - self.TILE_SIZE
                    rect = pygame.Rect(x, y, self.TILE_SIZE, self.TILE_SIZE)
                    self.collided_objects.append({"rect": rect, "type": symbol})




    def load_images(self):
        images = {}
        for symbol, path in self.SYMBOLS.items():
            if path:
                images[symbol] = pygame.image.load(path)
                images[symbol] = pygame.transform.scale(images[symbol], (self.TILE_SIZE, self.TILE_SIZE))
        return images

    def draw(self, screen):
        for row_idx, row in enumerate(self.grid):
            for col_idx, symbol in enumerate(row):
                if symbol in self.images:
                    x = (col_idx * self.TILE_SIZE) - self.offset
                    y = 450 - self.TILE_SIZE
                    screen.blit(self.images[symbol], (x, y))