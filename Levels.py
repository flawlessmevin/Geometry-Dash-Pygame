import pygame

class Level:
    TILE_SIZE = 50

    SYMBOLS = {
        "#": "assets/images/cube.png",
        "^": "assets/images/triangle.png",
        "@": "assets/images/portal.png",
        ".": None
    }

    def __init__(self, file_path):
        self.file_path = file_path
        self.collided_objects = []
        self.grid = []
        self.load_level()
        self.images = self.load_images()
        self.offset = 0
        self.level_length = 0

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
                    if symbol == "@":
                        rect = pygame.Rect(x, y - 150, self.TILE_SIZE * 2, self.TILE_SIZE * 2)
                    else:
                        rect = pygame.Rect(x, y, self.TILE_SIZE, self.TILE_SIZE)

                    self.collided_objects.append({"rect": rect, "type": symbol})

    def load_images(self):
        images = {}
        for symbol, path in self.SYMBOLS.items():
            if path:
                images[symbol] = pygame.image.load(path)
                if symbol == "@":
                    images[symbol] = pygame.transform.scale(images[symbol], (self.TILE_SIZE * 4, self.TILE_SIZE * 4))
                else:
                    images[symbol] = pygame.transform.scale(images[symbol], (self.TILE_SIZE, self.TILE_SIZE))
        return images

    def draw(self, screen):
        for obj in self.collided_objects:
            if obj["type"] in self.images:
                screen.blit(self.images[obj["type"]], (obj["rect"].x, obj["rect"].y))

    def get_progress(self):
        level_length = (len(self.grid[0]) * self.TILE_SIZE) - 150
        progress = (self.offset / level_length) * 100
        progress = min(progress, 100)
        return progress

    def draw_progress_bar(self, screen):
        progress = self.get_progress()
        bar_width = screen.get_width() * 0.8
        bar_height = 30

        pygame.draw.rect(screen, (50, 50, 50), (screen.get_width() * 0.1, 10, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (screen.get_width() * 0.1, 10, (bar_width * progress) / 100, bar_height))

        font = pygame.font.Font("assets/fonts/ARCADECLASSIC.TTF", 36)
        text = font.render(f"{int(progress)}", True, (255, 255, 255))

        text_x = screen.get_width() * 0.1 + bar_width / 2 - text.get_width() / 2
        text_y = 10 + (bar_height - text.get_height()) / 2
        screen.blit(text, (text_x, text_y))