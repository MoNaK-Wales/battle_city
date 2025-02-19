import pygame
import strategies
import constants
from time import time
from itertools import cycle
from abc import ABC, abstractmethod
from set_sprites import Entity
from logger import logger
from sounds_manager import SoundsManager


class Tank(Entity):
    def __init__(self, pos, src, strategy, speed, bullet_speed, anim_sprite):
        super().__init__(pos, src, strategy, speed)
        self.image = pygame.transform.scale_by(
            pygame.image.load(src), constants.TANK_SCALE * constants.SC_SCALE
        ).convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)
        self.bullet_speed = bullet_speed
        self.anims_iter = cycle([src, anim_sprite])
        self.lastanim = 0

    # def anim(self):
    #     if time() - self.lastanim > 0.1:
    #         self.image = pygame.transform.rotate(pygame.transform.scale_by(
    #             pygame.image.load(next(self.anims_iter)), constants.TANK_SCALE * constants.SC_SCALE
    #         ), self.angle)
    #         self.lastanim = time()
        

class Hero(Tank):
    def __init__(self, pos, hp=3):
        super().__init__(
            pos, "assets/sprites/tanks/hero_anim1.png", strategies.Controll_Strategy, 2, 2, "assets/sprites/tanks/hero_anim2.png"
        )

        self.hp = hp
        self.active_collectables = []
        self.spawnpoint = pos

    def change_spawnpoint(self, spawnpoint):
        if isinstance(spawnpoint, pygame.Vector2):
            self.spawnpoint = spawnpoint

    def move(self, obstacles, entities, hud):
        initial_pos = self.pos.copy()
        move = self.strategy.move(obstacles, entities, hud)
        # self.anim()
        SoundsManager.hero_running(self.pos, initial_pos)
        return move


class Enemy(Tank, ABC):
    def __init__(self, pos, src, strategy, speed, bullet_speed, anim_sprite):
        super().__init__(pos, src, strategy, speed, bullet_speed, anim_sprite)

    @abstractmethod
    def shoot(self):
        pass

    def update(self, entities, obstacles, hud):
        entities.remove(self)
        initial_pos = self.pos.copy()
        self.move(obstacles, entities, hud)
        # self.anim()
        SoundsManager.enemy_running(self.pos, initial_pos)
        self.rect.center = self.pos

    def kill(self):
        super().kill()
        SoundsManager.enemy_destroyed()

class SimpleEnemy(Enemy):
    def __init__(self, pos):
        super().__init__(pos, "assets/sprites/tanks/enemy1_anim1.png", strategies.Enemy_Strategy, 1, 1, "assets/sprites/tanks/enemy1_anim2.png")

    def shoot(self):
        pass

class FastEnemy(Enemy):
    def __init__(self, pos):
        super().__init__(pos, "assets/sprites/tanks/enemy2_anim1.png", strategies.Enemy_Strategy, 3, 2, "assets/sprites/tanks/enemy2_anim2.png")

    def shoot(self):
        pass


class TankFactory(ABC):
    def __init__(self, spawnpoint):
        self.spawnpoint = spawnpoint

    @abstractmethod
    def spawn(self):
        pass


class EnemyFactory(TankFactory):
    def __init__(self, spawnpoint, type_list):
        if not isinstance(spawnpoint, pygame.Vector2):
            logger.critical("Not correct spawnpoint")

        super().__init__(spawnpoint)
        self.enemy_type_dict = {0: SimpleEnemy, 1: FastEnemy}
        self.type_list = [self.enemy_type_dict[i](self.spawnpoint) for i in type_list]
        self.enemies_iter = iter(self.type_list)

    def spawn(self):
        return next(self.enemies_iter)
