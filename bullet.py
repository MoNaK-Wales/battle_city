import pygame
import constants
import strategies
from set_sprites import Entity
from sounds_manager import SoundsManager
from anims import Explosion


class Bullet(Entity):
    def __init__(self, pos, direction, is_real = False, bullets_group = None, expl_group = None, speed = 2, of_enemy = False):
        super().__init__( pos, "assets/sprites/bullet.png", strategies.BulletStrategy, speed)
        
        self.expl_group = expl_group
        self.speed = speed * constants.SPEED_BULLET * constants.SC_SCALE
        self.strategy = strategies.BulletStrategy(self, None, None, None, None, None)
        self.direction = direction
        self.of_enemy = of_enemy
        self.is_real = is_real
        self.is_overlap_entity = False  # пуле проверка при спавне не нужна
        if is_real:
            self.add(bullets_group)
            self.rotate(self.direction)
            SoundsManager.bullet_init()

    def update(self, **kwargs):
        super().update(**kwargs)
        self.move()
        self.rect.center = self.pos

    def kill(self):
        if self.is_real:
            Explosion(self.pos, "small", self.expl_group)
        super().kill()
