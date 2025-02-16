import pygame
import strategies
import constants
from abc import ABC, abstractmethod

# tile_size = 8
# big_tile_size = tile_size * 2

class Game_Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, src):
        super().__init__()

        self.pos = pygame.Vector2(pos)
        self.image = pygame.transform.scale_by(pygame.image.load(src), constants.sc_scale)
        self.rect = self.image.get_rect()

    def draw(self, screen):
        self.rect.center = self.pos
        screen.blit(self.image, self.rect)

class Entity(Game_Sprite):
    def __init__(self, pos, src, strategy, speed):
        super().__init__(pos, src)

        self.speed = 0.01 * speed * constants.sc_scale
        self.strategy = strategy(self)

        self.angle = 0
        self.angle_dict = {"up": 0, "right": 90, "down": 180, "left": 270}

    def move(self):
        self.strategy.move()

    def rotate(self, angle):
        target_angle = self.angle_dict[angle]
        delta_angle = target_angle - self.angle
        self.angle = target_angle
        self.image = pygame.transform.rotate(self.image, -delta_angle)
        self.rect = self.image.get_rect(center=self.rect.center)

class Hero(Entity):
    def __init__(self, pos, hp):
        super().__init__(pos, "assets/tanks/hero_anim1.png", strategies.Controll_Strategy, 2)

        self.hp = hp
        self.active_collectables = []
        self.spawnpoint = pos

    def change_spawnpoint(self, spawnpoint):
        if isinstance(spawnpoint, pygame.Vector2):
            self.spawnpoint = spawnpoint
    

class Obstacle(Game_Sprite):
    pass

class Brick(Obstacle):
    def __init__(self, pos):
        super().__init__(pos, "assets/blocks/brick.png")
    
    # ДОБАВИТЬ после пуль
    # def destroy():
    #     pass

class Wall(Obstacle):
    def __init__(self, pos):
        super().__init__(pos, "assets/blocks/wall.png")

class Base(Obstacle):
    def __init__(self, pos):
        super().__init__(pos, "assets/blocks/base.png")

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