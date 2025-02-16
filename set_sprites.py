import pygame
import strategies
import constants
from abc import ABC, abstractmethod
from main import *

class Game_Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, src):
        super().__init__()

        self.pos = pygame.Vector2(pos)
        self.image = pygame.transform.scale_by(pygame.image.load(src), constants.sc_scale).convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)

    def draw(self, screen):
        self.rect.center = self.pos
        screen.blit(self.image, self.rect)


class Entity(Game_Sprite):
    def __init__(self, pos, src, strategy, speed):
        super().__init__(pos, src)

        self.speed = constants.speed * speed * constants.sc_scale
        self.strategy = strategy(self)

        self.angle = 0
        self.angle_dict = {
            "up": (0, False),
            "right": (90, False),
            "down": (180, True),
            "left": (270, True),
        }
        self.is_mirrored = False  # при нижнем и правом положении спрайт отзеркален

    def move(self, obstacles):
        self.strategy.move(obstacles)

    def rotate(self, angle):
        target_angle, target_mirror = self.angle_dict[angle]
        delta_angle = target_angle - self.angle
        self.angle = target_angle

        self.image = pygame.transform.rotate(self.image, -delta_angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.is_mirrored != target_mirror:
            if target_angle == 180 or target_angle == 0:
                self.image = pygame.transform.flip(self.image, True, False)
            elif target_angle == 270 or target_angle == 90:
                self.image = pygame.transform.flip(self.image, False, True)

            self.is_mirrored = target_mirror


class Hero(Entity):
    def __init__(self, pos, hp=3):
        super().__init__(
            pos, "assets/tanks/hero_anim1.png", strategies.Controll_Strategy, 2
        )

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
        if not (isinstance(entity, Entity) and (isinstance(obstacle, Obstacle) or isinstance(obstacle, pygame.Rect))):
            raise TypeError("First arg must be Entity, the second one must be Obstacle (or just Rect for HUD)")

        if isinstance(obstacle, pygame.Rect):
            return entity.rect.colliderect(obstacle)
        # if isinstance(entity, Hero): #or isinstance(entity, Enemy)
        #     return True
        # elif isinstance(entity, Bullet):
        #     if isinstance(obstacle, Water):
        #         return False
        #     elif isinstance(obstacle, Brick):
        #         obstacle.destroy()
        #         return True
        #     else:
        #         return True
        raise TypeError("Not correct Entity object")
