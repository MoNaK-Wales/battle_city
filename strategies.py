import random
import pygame
import pygame.math
import set_sprites
from time import *
from abc import ABC, abstractmethod
from constants import *
from bullet import Bullet
from collide_manager import CollideManager
from logger import logger

class MoveStrategy(ABC):
    def __init__(self, entity, obstacles, entities, hud, bullets, anims):
        if not isinstance(entity, set_sprites.Entity):
            raise TypeError("Not an Entity")

        self.entity = entity
        self.speed = self.entity.speed
        
        self.obstacles = obstacles
        self.entities = entities
        self.hud = hud
        self.bullets = bullets
        self.anims = anims

        self.directions = {
            "down": (0, self.speed),
            "right": (self.speed, 0),
            "up": (0, -self.speed),
            "left": (-self.speed, 0),
        }
        self.last_shot = 0
        self.bullet_pos = {
            0: (0, -TILE_SIZE),
            90: (TILE_SIZE, 0),
            180: (0, TILE_SIZE),
            270: (-TILE_SIZE, 0),
        }

    # логика движения
    @abstractmethod
    def move(self):
        pass

    # обработка движения
    def move_entity(self, direction_name):
        new_pos = self.entity.pos + self.directions[direction_name]

        future_entity = self.entity.__class__(new_pos)
        if future_entity.__class__.__name__.endswith("Enemy"):
            future_entity.is_overlap_player = self.entity.is_overlap_player

        collides = [
            CollideManager.checkCollide(future_entity, obstacle)
            for obstacle in self.obstacles
        ]
        collides += [
            CollideManager.checkCollide(future_entity, hud_rect)
            for hud_rect in self.hud
        ]
        collides += [
            CollideManager.checkCollideEntities(future_entity, entity)
            for entity in self.entities
        ]

        if not any(collides):
            self.entity.pos = new_pos
        if self.entity.angle != self.entity.angle_dict[direction_name][0]:
            self.entity.rotate(direction_name)


class ControllStrategy(MoveStrategy):
    def move(self):
        keys = pygame.key.get_pressed()

        # рух гравця по клавішам
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move_entity("up")
            self.entity.anim()
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move_entity("down")
            self.entity.anim()
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.move_entity("left")
            self.entity.anim()
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.move_entity("right")
            self.entity.anim()

        # стрільба
        if (keys[pygame.MOUSEBUTTONDOWN] or keys[pygame.K_x]) and time() - self.last_shot > 0.85:
            bullet_pos = pygame.Vector2(self.entity.rect.center) + pygame.Vector2(self.bullet_pos[self.entity.angle])
            Bullet(bullet_pos, self.entity.angle, True, self.bullets, self.anims, 2)
            self.last_shot = time()


class EnemyStrategy(MoveStrategy):
    # легкий - случайно идёт
    # normal 1/8 - идет к базе, 1/4 - случайно идет, 5/8 - идёт к игроку
    # hard 2/7 - идёт к базе, 1/7 - случайно идёт, 4/7 - идёт к игроку
    # все танки меняют направление раз в 0.5 секунд, стреляют раз в 4/3 секунд (сильный - раз в 2/3)

    def __init__(self, entity, obstacles, entities, hud, bullets, anims):
        super().__init__(entity, obstacles, entities, hud, bullets, anims)

        self.move_timer = 0  # Счётчик кадров
        self.move_delay = FPS * 0.5
        self.shoot_delay = entity.shoot_delay
        self.direction_keys = list(self.directions.keys())
        self.random_direction = random.choice(self.direction_keys)

    def move(self):
        self.move_entity(self.random_direction)
        self.entity.anim()
        if self.move_timer >= self.move_delay:
            self.random_direction = random.choice(self.direction_keys)
            self.move_timer = 0
            self.move_delay = random.randint(10, 50)
        else:
            self.move_timer += 1

    # def fire(self):


# class EnemyEasyStrategy(EnemyStrategy):    
#     def move(self):
#         self.move_entity(self.random_direction)
#         self.entity.anim()

#         if self.move_timer >= self.move_delay:
#             self.random_direction = random.choice(self.direction_keys)
#             self.move_timer = 0
#         else:
#             self.move_timer += 1

        


class BulletStrategy(MoveStrategy):
    def move_entity(self, direction_name):
        new_pos = self.entity.pos + self.directions[direction_name]

        future_bullet = Bullet(new_pos, self.entity.angle_dict[direction_name][0])
        collides = [
            CollideManager.checkCollide(future_bullet, obstacle)
            for obstacle in self.obstacles
        ]
        collides += [
            CollideManager.checkCollide(future_bullet, hud_rect)
            for hud_rect in self.hud
        ]
        collides += [
            CollideManager.checkCollideEntities(future_bullet, entity)
            for entity in self.entities
        ]

        if not any(collides):
            self.entity.pos = new_pos
        else:
            self.entity.kill()

    def move(self):
        if self.entity.direction == 0:
            self.move_entity("up")
        if self.entity.direction == 90:
            self.move_entity("right")
        if self.entity.direction == 180:
            self.move_entity("down")
        if self.entity.direction == 270:
            self.move_entity("left")

class NoMovement(MoveStrategy):
    def __init__(self):
        pass
    def move(self):
        pass
