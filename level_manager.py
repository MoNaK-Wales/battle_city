import pygame
from os import path
from constants import *
from set_sprites import *


class LevelLoader:
    TILE_SIZE = 8 * SC_SCALE
    OFFSET = pygame.Vector2(OFFS_OBJ * SC_SCALE, OFFS_OBJ * SC_SCALE)
    CENTER = (TILE_SIZE, TILE_SIZE) - (OFFSET - (HUD_WIDTH, HUD_WIDTH))

    SYMBOLS = {
        "#": Brick,
        "@": Wall,
        "%": Foliage,
        "H": pygame.Vector2,
        "E": pygame.Vector2
    }

    def __init__(self, filename):
        logger.debug(f"Loading level from {filename}")
        if not path.isfile(filename):
            raise FileNotFoundError(filename)

        self.filename = filename
        self.objects = []
        self.enemy_spawns = []
        self.spawnpoint = None

    def load(self):
        with open(self.filename, "r") as file:
            level_map = [line.strip() for line in file.readlines()]

        for row_idx, row in enumerate(level_map):
            for col_idx, cell in enumerate(row):
                x = col_idx * self.TILE_SIZE + self.OFFSET.x
                y = row_idx * self.TILE_SIZE + self.OFFSET.y

                if cell in self.SYMBOLS:
                    if cell == "H":
                        self.spawnpoint = self.SYMBOLS[cell](x, y) + self.CENTER
                    elif cell == "E":
                        self.enemy_spawns.append(self.SYMBOLS[cell](x, y) + self.CENTER)
                    else:
                        self.objects.append(self.SYMBOLS[cell]((x, y)))

        return self.objects, self.spawnpoint, self.enemy_spawns
