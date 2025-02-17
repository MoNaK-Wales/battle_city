import pygame
import strategies
import constants
from abc import ABC, abstractmethod
from set_sprites import Entity


class Enemy(Entity, ABC):
    def __init__(self, pos, src, strategy, speed, bullet_speed):
        super().__init__(pos, src, strategy, speed)
        self.bullet_speed = bullet_speed
        self.rect = self.image.get_rect(topleft=self.pos) #уменьшать спрайты по коэффициенту
    
    def update(self):
        self.rect.topleft = self.pos
        constants.logger.debug(f"x: {self.rect.x}, y: {self.rect.y}")

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