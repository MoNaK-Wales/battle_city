import pygame
import strategies
import constants
from time import time
from itertools import cycle
from abc import ABC, abstractmethod
from set_sprites import Entity
from logger import logger
from anims import Explosion, SpawnAnim
from sounds_manager import SoundsManager
from score_manager import ScoreManager


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


class Hero(Tank):
    sprite1 = "assets/sprites/tanks/hero_anim1.png"
    sprite2 = "assets/sprites/tanks/hero_anim2.png"
    strategy = strategies.ControllStrategy

    def __init__(self, pos, expl_group = None, factory = None):
        super().__init__(pos, self.sprite1, self.sprite2, self.strategy, 2, 2, expl_group)

        self.hp = 3
        self.factory = factory
        self.active_collectables = []

    def update(self, **kwargs):
        initial_pos = self.pos.copy()

        super().update(**kwargs)
        self.move()
        self.rect.center = self.pos

        SoundsManager.hero_running(self.pos, initial_pos)
    
    def kill(self):
        super().kill()
        SoundsManager.player_destroyed()

        self.hp -= 1
        Explosion(self.pos, "big", self.expl_group, self.factory.spawn).update()


class Enemy(Tank, ABC):
    def __init__(self, pos, src, anim_sprite, strategy, speed, bullet_speed, shoot_delay, expl_group = None):
        super().__init__(pos, src, anim_sprite, strategy, speed, bullet_speed, expl_group)

        self.shoot_delay = shoot_delay

    def update(self, **kwargs):
        super().update(**kwargs)

        self.move()
        self.rect.center = self.pos

        SoundsManager.enemy_running(True)     

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
        Explosion(self.pos, "big", self.expl_group)

class SimpleEnemy(Enemy):
    sprite1 = "assets/sprites/tanks/enemy1_anim1.png"
    sprite2 = "assets/sprites/tanks/enemy1_anim2.png"
    strategy = strategies.EnemyEasyStrategy
    shoot_delay = 4/3 * constants.FPS

    def __init__(self, pos, expl_group = None):
        super().__init__(pos, self.sprite1, self.sprite2, self.strategy, 1, 1, self.shoot_delay, expl_group)

    def kill(self):
        super().kill()
        ScoreManager.add("Simple")

class FastEnemy(Enemy):
    sprite1 = "assets/sprites/tanks/enemy2_anim1.png"
    sprite2 = "assets/sprites/tanks/enemy2_anim2.png"
    strategy = strategies.EnemyHardStrategy
    shoot_delay = 4/3 * constants.FPS

    def __init__(self, pos, expl_group = None):
        super().__init__(pos, self.sprite1, self.sprite2, self.strategy, 3, 2, self.shoot_delay, expl_group)

    def kill(self):
        super().kill()
        ScoreManager.add("Fast")

class PowerEnemy(Enemy):
    sprite1 = "assets/sprites/tanks/enemy3_anim1.png"
    sprite2 = "assets/sprites/tanks/enemy3_anim2.png"
    strategy = strategies.EnemyNormalStrategy
    shoot_delay = 2/3 * constants.FPS

    def __init__(self, pos, expl_group = None):
        super().__init__(pos, self.sprite1, self.sprite2, self.strategy, 2, 3, self.shoot_delay, expl_group)

    def kill(self):
        super().kill()
        ScoreManager.add("Power")

class ArmorEnemy(Enemy):
    sprite1 = "assets/sprites/tanks/enemy4_anim1.png"
    sprite2 = "assets/sprites/tanks/enemy4_anim2.png"
    strategy = strategies.EnemyNormalStrategy
    shoot_delay = 4/3 * constants.FPS

    def __init__(self, pos, expl_group = None):
        super().__init__(pos, self.sprite1, self.sprite2, self.strategy, 2, 2, self.shoot_delay, expl_group)
        self.hp = 4

    def kill(self):
        self.hp -= 1
        if self.hp == 0:
            super().kill()
            ScoreManager.add("Armor")
        else:
            SoundsManager.bullet_wall()


class TankFactory(ABC):
    def __init__(self, spawnpoint, anims_group):
        if not isinstance(spawnpoint, pygame.Vector2):
            logger.critical("Not correct spawnpoint")

        self.spawnpoint = spawnpoint
        self.anims_group = anims_group

    @abstractmethod
    def spawn(self, group):
        pass


class EnemyFactory(TankFactory):
    def __init__(self, spawnpoint, anims_group, type_list):
        super().__init__(spawnpoint, anims_group)
        self.enemy_type_dict = {0: SimpleEnemy, 1: FastEnemy, 2: PowerEnemy, 3: ArmorEnemy}
        self.type_list = [self.enemy_type_dict[i](self.spawnpoint, self.anims_group) for i in type_list]
        self.enemies_iter = iter(self.type_list)

    def spawn(self, enemies_group):
        def create_enemy():
            new_enemy = next(self.enemies_iter)
            enemies_group.add(new_enemy)
            logger.info(f"{type(new_enemy)} object spawned")

        SpawnAnim(self.spawnpoint, self.anims_group, create_enemy)


class HeroFactory(TankFactory):
    def __init__(self, spawnpoint, anims_group, hero_group, gameover_func):
        super().__init__(spawnpoint, anims_group)
        self.hero_group = hero_group
        self.hero = Hero(self.spawnpoint, self.anims_group, self)
        self.gameover_func = gameover_func

    def spawn(self):
        def create_hero():
            self.hero.pos = self.spawnpoint
            self.hero_group.add(self.hero)
            logger.info("Hero spawned")

        if self.hero.hp > 0:
            SpawnAnim(self.spawnpoint, self.anims_group, create_hero).update()
        else:
            self.gameover_func()