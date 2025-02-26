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
        "B": pygame.Vector2,
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
        self.base_pos = None
        self.enemy_types = []

    def load(self):
        with open(self.filename, "r") as file:
            level_map = [line.strip() for line in file.readlines()]

        for row_idx, row in enumerate(level_map[:-3]):
            for col_idx, cell in enumerate(row):
                x = col_idx * self.TILE_SIZE + self.OFFSET.x
                y = row_idx * self.TILE_SIZE + self.OFFSET.y

                if cell in self.SYMBOLS:
                    if cell == "H":
                        self.spawnpoint = self.SYMBOLS[cell](x, y) + self.CENTER
                    elif cell == "B":
                        self.base_pos = self.SYMBOLS[cell](x, y) + self.CENTER
                    elif cell == "E":
                        self.enemy_spawns.append(self.SYMBOLS[cell](x, y) + self.CENTER)
                    else:
                        self.objects.append(self.SYMBOLS[cell]((x, y)))

        for row in level_map[-3:]:
            enemy_row = [int(char) for char in row]
            self.enemy_types.append(enemy_row)

        return self.objects, self.spawnpoint, self.base_pos, self.enemy_spawns, self.enemy_types
