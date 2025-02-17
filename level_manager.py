import pygame
from os import path
from constants import *
from set_sprites import *


class LevelLoader:
    TILE_SIZE = 8 * sc_scale
    OFFSET = pygame.Vector2(offs_obj * sc_scale, offs_obj * sc_scale)

    SYMBOLS = {
        "#": Brick,
        "@": Wall,
        "L": Foliage,
        "H": pygame.Vector2
    }

    def __init__(self, filename):
        if not path.isfile(filename):
            raise FileNotFoundError(filename)
        
        self.filename = filename
        self.objects = []
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
                        self.spawnpoint = self.SYMBOLS[cell](x, y)
                    else:
                        self.objects.append(self.SYMBOLS[cell]((x, y)))

        return self.objects, self.spawnpoint


# level1 = LevelLoader("assets/stages/stage1")
# objects = level1.load()


# def drTest():
#     for obj in objects:
#         obj.draw(screen)
