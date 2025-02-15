import pygame
import strategies
from abc import ABC, abstractmethod

tile_size = 8
big_tile_size = tile_size * 2

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
    def __init__(self, pos, hp, spawnpoint):
        super().__init__(pos, big_tile_size, big_tile_size, "assets/tanks/hero_anim1.png", strategies.Controll_Strategy(self), 2)

        self.hp = hp
        self.active_collectables = []
        self.spawnpoint = spawnpoint

    def change_spawnpoint(self, spawnpoint):
        if isinstance(spawnpoint, pygame.Vector2):
            self.spawnpoint = spawnpoint

class Obstacle(Game_Sprite):
    pass

class Brick(Obstacle):
    def __init__(self, pos):
        super().__init__(pos, tile_size, tile_size, "assets/blocks/brick.png")
    
    # ДОБАВИТЬ после пуль
    # def destroy():
    #     pass

class Wall(Obstacle):
    def __init__(self, pos):
        super().__init__(pos, tile_size, tile_size, "assets/blocks/wall.png")

class Base(Obstacle):
    def __init__(self, pos):
        super().__init__(pos, big_tile_size, big_tile_size, "assets/blocks/base.png")

    # ДОБАВИТЬ смерть после пуль


class CollideManager:
    @staticmethod
    def checkCollide(entity, obstacle):
        if not (isinstance(entity, Entity) and isinstance(obstacle, Obstacle)):
            raise TypeError("First arg must be Entity, the second one must be Obstacle")
        
        if isinstance(entity, Hero): #or isinstance(entity, Enemy)
            return True
        # elif isinstance(entity, Bullet):
        #     if isinstance(obstacle, Water):
        #         return False
        #     elif isinstance(obstacle, Brick):
        #         obstacle.destroy()
        #         return True
        #     else:
        #         return True
        raise TypeError("Not correct Entity object")