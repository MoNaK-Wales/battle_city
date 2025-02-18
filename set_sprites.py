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

    def update(self):
        self.rect.center = self.pos


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
            0: (0, False),
            90: (90, False),
            180: (180, True),
            270: (270, True),
        }
        self.is_mirrored = False  # при нижнем и правом положении спрайт отзеркален

    def move(self, obstacles, entitys, enemy):
        self.strategy.move(obstacles, entitys, enemy)

    def rotate(self, angle):
        constants.logger.info(f"Rotating {angle} {self}")
        target_angle, target_mirror = self.angle_dict[angle]
        delta_angle = target_angle - self.angle
        self.angle = target_angle
        constants.logger.debug(f"Target angle - {target_angle}; delta - {delta_angle}")

        self.image = pygame.transform.rotate(self.image, -delta_angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.is_mirrored != target_mirror:
            constants.logger.debug("Sprite must be mirrored")
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

    def move(self, obstacles, entitys, enemy, bullet_group):
        self.strategy.move(obstacles, entitys, enemy, bullet_group)

    def change_spawnpoint(self, spawnpoint):
        if isinstance(spawnpoint, pygame.Vector2):
            self.spawnpoint = spawnpoint

class Enemy(Entity):
    def __init__(self, pos, hp=3):
        super().__init__(
            pos, "assets/tanks/hero_anim1.png", strategies.Enemy_Strategy, 2
        )

        self.hp = hp
        self.active_collectables = []
        self.spawnpoint = pos

    def change_spawnpoint(self, spawnpoint):
        if isinstance(spawnpoint, pygame.Vector2):
            self.spawnpoint = spawnpoint

class Bullet(Entity):
    def __init__(self, pos, direction, speed = 2):
        speed *= constants.speed_bullet * constants.sc_scale
        super().__init__( pos, "assets/sprites/bullet.png", strategies.Bullet_strategy, speed)
        self.direction = direction
        

    def update(self, obstacles, entitys, enemy):
        self.rect.center = self.pos
        self.move(obstacles, entitys, enemy)
    
    def kill(self):
        # anim.play
        super().kill()


class Obstacle(Game_Sprite):
    def __init__(self, pos, src):
        super().__init__(pos, src)
        constants.logger.debug(f"Created {type(self)} obstacle on {pos}")


class Brick(Obstacle):
    def __init__(self, pos):
        super().__init__(pos, "assets/blocks/brick.png")

    # ДОБАВИТЬ после пуль
    # def destroy():
    #     pass


class Wall(Obstacle):
    def __init__(self, pos):
        super().__init__(pos, "assets/blocks/wall.png")

class Foliage(Obstacle):
    def __init__(self, pos):
        super().__init__(pos, "assets/blocks/foliage.png")

class Base(Obstacle):
    def __init__(self, pos):
        super().__init__(pos, "assets/blocks/base.png")

    # ДОБАВИТЬ смерть после пуль


class CollideManager:
    @staticmethod
    def checkCollide(entity, obstacle):
        if not (isinstance(entity, Entity) and isinstance(obstacle, (Obstacle, pygame.Rect))):
            constants.logger.critical(f"CollideManager take Entity and Obstacle/Rect, but {type(entity)} and {type(obstacle)} are given")
            raise TypeError("First arg must be Entity, the second one must be Obstacle (or just Rect for HUD)")

        if isinstance(obstacle, (pygame.Rect, Wall, Brick)):
            collide = entity.rect.colliderect(obstacle)
            # if isinstance(entity, Bullet), isinstance(obstacle, Wall):
            #     obstacle.destroy()
            return collide
        elif isinstance(obstacle, Foliage):
            return False

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

        constants.logger.error("Not correct Entity object was given, returning False")
        return False
    @staticmethod
    def checkCollideEntities(entity1, entity2):
        if not (isinstance(entity1, Entity) and isinstance(entity2, Entity)):
            constants.logger.critical(f"checkCollideEntities takes 2 Entity objects, but {type(entity1)} and {type(entity2)} are given")
            raise TypeError("Both args must be Entity")

        collide = entity1.rect.colliderect(entity2)
        return collide