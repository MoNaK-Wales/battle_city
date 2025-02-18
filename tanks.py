import pygame
import strategies
import constants
from abc import ABC, abstractmethod
from set_sprites import Entity


class Tank(Entity):
    def __init__(self, pos, src, strategy, speed, bullet_speed):
        super().__init__(pos, src, strategy, speed)
        self.image = pygame.transform.scale_by(pygame.image.load(src), constants.tank_scale * constants.sc_scale).convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)
        self.bullet_speed = bullet_speed


class Hero(Tank):
    def __init__(self, pos, hp=3):
        super().__init__(
            pos, "assets/tanks/hero_anim1.png", strategies.Controll_Strategy, 2, 2
        )

        self.hp = hp
        self.active_collectables = []
        self.spawnpoint = pos

    def change_spawnpoint(self, spawnpoint):
        if isinstance(spawnpoint, pygame.Vector2):
            self.spawnpoint = spawnpoint
    

class Enemy(Tank, ABC):
    def __init__(self, pos, src, strategy, speed, bullet_speed):
        super().__init__(pos, src, strategy, speed, bullet_speed)

    @abstractmethod
    def shoot(self):
        pass

    def explode(self):
        self.kill()

class SimpleEnemy(Enemy):
    def __init__(self, pos):
        super().__init__(pos, "assets/tanks/enemy1_anim1.png", strategies.Enemy_Strategy, 1, 1)

    def shoot(self):
        pass

class FastEnemy(Enemy):
    def __init__(self, pos):
        super().__init__(pos, "assets/tanks/enemy2_anim1.png", strategies.Enemy_Strategy, 3, 2)

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
            constants.logger.critical("Not correct spawnpoint")

        super().__init__(spawnpoint)
        self.enemy_type_dict = {0: SimpleEnemy, 1: FastEnemy}
        self.type_list = [self.enemy_type_dict[i](self.spawnpoint) for i in type_list]
        self.enemies_iter = iter(self.type_list)

    def spawn(self):
        return next(self.enemies_iter)