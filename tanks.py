import pygame
import strategies
import constants
from time import time
from itertools import cycle
from abc import ABC, abstractmethod
from set_sprites import Entity
from logger import logger
from collide_manager import CollideManager
from sounds_manager import SoundsManager
from anims import Explosion, SpawnAnim


class Tank(Entity):
    scale = constants.TANK_SCALE * constants.SC_SCALE

    def __init__(self, pos, src, anim_sprite, strategy, speed, bullet_speed, expl_group):
        super().__init__(pos, src, strategy, speed)

        self.image = pygame.transform.scale_by(pygame.image.load(src), self.scale).convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)

        self.bullet_speed = bullet_speed

        self.anims_iter = cycle([src, anim_sprite])
        self.delay = 0.06
        self.lastanim = 0

        self.expl_group = expl_group

    def update(self, **kwargs):
        super().update(**kwargs)

    def anim(self):
        if time() - self.lastanim > self.delay:
            next_img = next(self.anims_iter)
            self.original_image = pygame.transform.scale_by(pygame.image.load(next_img), self.scale).convert_alpha()
            self.rotate(self.angle)
            self.lastanim = time()

    def kill(self):
        super().kill()
        Explosion(self.pos, "big", self.expl_group)


class Hero(Tank):
    sprite1 = "assets/sprites/tanks/hero_anim1.png"
    sprite2 = "assets/sprites/tanks/hero_anim2.png"
    strategy = strategies.ControllStrategy

    def __init__(self, pos, hp=3, expl_group = None):
        super().__init__(pos, self.sprite1, self.sprite2, self.strategy, 2, 2, expl_group)

        self.hp = hp
        self.active_collectables = []
        self.spawnpoint = pos

    def change_spawnpoint(self, spawnpoint):
        if isinstance(spawnpoint, pygame.Vector2):
            self.spawnpoint = spawnpoint

    def update(self, **kwargs):
        initial_pos = self.pos.copy()

        super().update(**kwargs)
        self.strategy.move()
        self.rect.center = self.pos

        SoundsManager.hero_running(self.pos, initial_pos)
    
    def kill(self):
        super().kill()
        SoundsManager.player_destroyed()


class Enemy(Tank, ABC):
    def __init__(self, pos, src, anim_sprite, strategy, speed, bullet_speed, shoot_delay, expl_group = None):
        super().__init__(pos, src, anim_sprite, strategy, speed, bullet_speed, expl_group)

        self.shoot_delay = shoot_delay

        # при спавне враг будет считаться находящимся внутри игрока, и только после выхода из него (может сразу при спавне) 
        # флаг отключается и может проверяться коллизия
        self.is_overlap_player = True

    @abstractmethod
    def shoot(self):
        pass

    def update(self, **kwargs):
        if self.is_overlap_player:
            hero = self.find_hero(kwargs["entities"])
            if hero is None:
                self.is_overlap_player = False
            else:
                self.check_player_overlapping(hero)

        entities_copy = kwargs["entities"].copy()
        entities_copy.remove(self)
        new_kwargs = kwargs.copy()
        new_kwargs.update(entities=entities_copy)
        super().update(**new_kwargs)
        self.move()
        self.rect.center = self.pos

        SoundsManager.enemy_running(True)

    def check_player_overlapping(self, hero):
        if not self.rect.colliderect(hero.rect):
            self.is_overlap_player = False

    def find_hero(self, entities):
        hero = None
        for entity in entities:
            if isinstance(entity, Hero):
                hero = entity
                break
        return hero

    def kill(self):
        super().kill()
        SoundsManager.enemy_running(False)
        SoundsManager.enemy_destroyed()

class SimpleEnemy(Enemy):
    sprite1 = "assets/sprites/tanks/enemy1_anim1.png"
    sprite2 = "assets/sprites/tanks/enemy1_anim2.png"
    strategy = strategies.EnemyStrategy
    shoot_delay = 4/3 * constants.FPS

    def __init__(self, pos, expl_group = None):
        super().__init__(pos, self.sprite1, self.sprite2, self.strategy, 1, 1, self.shoot_delay, expl_group)

    def shoot(self):
        pass

class FastEnemy(Enemy):
    sprite1 = "assets/sprites/tanks/enemy2_anim1.png"
    sprite2 = "assets/sprites/tanks/enemy2_anim2.png"
    strategy = strategies.EnemyStrategy
    shoot_delay = 4/3 * constants.FPS

    def __init__(self, pos, expl_group = None):
        super().__init__(pos, self.sprite1, self.sprite2, self.strategy, 3, 2, self.shoot_delay, expl_group)

    def shoot(self):
        pass


class TankFactory(ABC):
    def __init__(self, spawnpoint):
        self.spawnpoint = spawnpoint

    @abstractmethod
    def spawn(self):
        pass


class EnemyFactory(TankFactory):
    def __init__(self, spawnpoint, type_list, anims_group):
        if not isinstance(spawnpoint, pygame.Vector2):
            logger.critical("Not correct spawnpoint")

        super().__init__(spawnpoint)
        self.anims_group = anims_group
        self.enemy_type_dict = {0: SimpleEnemy, 1: FastEnemy}
        self.type_list = [self.enemy_type_dict[i](self.spawnpoint, anims_group) for i in type_list]
        self.enemies_iter = iter(self.type_list)

    def spawn(self, enemies_group):
        def create_enemy():
            new_enemy = next(self.enemies_iter)
            enemies_group.add(new_enemy)
            logger.info(f"{type(new_enemy)} object spawned")

        SpawnAnim(self.spawnpoint, self.anims_group, create_enemy)
