import os



SETTINGS_FILE = "Settings.txt"


settings = {}
with open(SETTINGS_FILE, "r") as file:
    for line in file:
        if "=" in line:
            key, value = line.strip().split(" = ", 1)
            settings[key] = value




SCREEN_WIDTH = int(settings.get("SCREEN_WIDTH", 800))
SCREEN_HEIGHT = int(settings.get("SCREEN_HEIGHT", 600))
TILE_SIZE = int(settings.get("TILE_SIZE", 50))

LEVEL_LENGTH = int(settings.get("LEVEL_LENGTH", 20))




FONT = "assets/fonts/ARCADECLASSIC.TTF"

PLAYER_IMAGES = ["assets/images/sprite.png",
                 "assets/images/sprite_jumping.png"
                ]




