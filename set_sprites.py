import pygame
from abc import ABC, abstractmethod

class Game_Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, width, height, src):
        super().__init__()
        self.pos = pos
        self.width = width
        self.height = height
        self.direction_dict = {"up"}
        self.image = pygame.transform.scale(pygame.image.load(src), (width, height))
        self.rect = self.image.get_rect()

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

class Entity(Game_Sprite):
    def __init__(self, pos, width, height, src, strategy, speed):
        super().__init__(pos, width, height, src)

        self.strategy = strategy
        self.speed = speed

    def move(self):
        self.strategy.move()

class Hero(Entity):
    def __init__(self, pos, width, height, src, strategy, speed, hp, spawnpoint):
        super().__init__(pos, width, height, src, strategy, speed)

        self.hp = hp
        self.active_collectables = []
        self.spawnpoint = spawnpoint

    def change_spawnpoint(self, spawnpoint):
        if isinstance(spawnpoint, pygame.Vector2):
            self.spawnpoint = spawnpoint

class Obstacles(Game_Sprite):
    @abstractmethod
    def collide(self, entity):
        pass

class Wall(Obstacles):
    def __init__(self, pos, width, height, src = "assets/blocks/brick.png"):
        super().__init__(pos, width, height, src)

    def collide(self, entity):
        if isinstance(entity, Hero):
            pass