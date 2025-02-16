from constants import *
from set_sprites import *
from pygame import *
from main import *







class LevelLoader:
    TILE_SIZE = 8 * sc_scale  
    OFFSET = pygame.Vector2(offs_obj * sc_scale, offs_obj * sc_scale)  

    SYMBOLS = {
        "#": Brick,
        "@": Wall,
    }

    def __init__(self, filename):
        self.filename = filename
        self.objects = []

    def load(self):
        with open(self.filename, "r") as file:
            level_map = [line.strip() for line in file.readlines()]

        for row_idx, row in enumerate(level_map):
            for col_idx, cell in enumerate(row):
                x = col_idx * self.TILE_SIZE + self.OFFSET.x
                y = row_idx * self.TILE_SIZE + self.OFFSET.y

                if cell in self.SYMBOLS:
                    self.objects.append(self.SYMBOLS[cell]((x, y)))

        return self.objects

level1 = LevelLoader("assets/stages/stage1") 
objects = level1.load()
def drTest():
    for obj in objects:
        obj.draw(screen)