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

class Move_Strategy(ABC):
    def __init__(self, entity):
        if not isinstance(entity, set_sprites.Entity):
            raise TypeError("Not an Entity")

        self.entity = entity
        self.speed = self.entity.speed

        self.directions = {
            "down": (0, self.speed),
            "right": (self.speed, 0),
            "up": (0, -self.speed),
            "left": (-self.speed, 0),
        }

    # логика движения
    @abstractmethod
    def move(self, obstacles, entities, hud):
        pass

    # обработка движения
    def move_entity(self, direction_name, obstacles, entities, hud):
        new_pos = self.entity.pos + self.directions[direction_name]

        future_entity = self.entity.__class__(new_pos)
        collides = [
            CollideManager.checkCollide(future_entity, obstacle)
            for obstacle in obstacles
        ]
        collides += [
            CollideManager.checkCollide(future_entity, hud_rect)
            for hud_rect in hud
        ]
        collides += [
            CollideManager.checkCollideEntities(future_entity, entity)
            for entity in entities
        ]

        if not any(collides):
            self.entity.pos = new_pos
        if self.entity.angle != self.entity.angle_dict[direction_name][0]:
            self.entity.rotate(direction_name)


class Controll_Strategy(Move_Strategy):
    def __init__(self, entity):
        super().__init__(entity)
        self.last_shot = 0
        self.bullet_pos = {
            0: (0, -TILE_SIZE),
            90: (TILE_SIZE, 0),
            180: (0, TILE_SIZE),
            270: (-TILE_SIZE, 0),
        }

    def move(self, obstacles, enemies, hud):
        keys = pygame.key.get_pressed()

        # добавити паузу!!!!!!!!
        if keys[pygame.K_ESCAPE] or keys[pygame.K_KP_ENTER]:
            logger.info("Pause")
            global PAUSE
            PAUSE = True

        # рух гравця по клавішам
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move_entity("up", obstacles, enemies, hud)
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move_entity("down", obstacles, enemies, hud)
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.move_entity("left", obstacles, enemies, hud)
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.move_entity("right", obstacles, enemies, hud)

        # стрільба
        if (keys[pygame.MOUSEBUTTONDOWN] or keys[pygame.K_x]) and time() - self.last_shot > 0.85:
            bullet = Bullet(pygame.Vector2(self.entity.rect.center) + pygame.Vector2(self.bullet_pos[self.entity.angle]), self.entity.angle, 2)
            self.last_shot = time()
            return bullet

        return None


class Enemy_Strategy(Move_Strategy):

    def __init__(self, entity):
        super().__init__(entity)

        self.move_timer = 0  # Счётчик кадров
        self.move_delay = random.randint(10, 50)
        self.random_direction = random.choice(["up", "down", "left", "right"])

    def move(self, obstacles, entities, hud):
        self.move_entity(self.random_direction, obstacles, entities, hud)
        if self.move_timer >= self.move_delay:
            self.random_direction = random.choice(["up", "down", "left", "right"])
            self.move_timer = 0
            self.move_delay = random.randint(10, 50)
        else:
            self.move_timer += 1


class Bullet_strategy(Move_Strategy):
    def move_entity(self, direction_name, obstacles, entities, hud):
        new_pos = self.entity.pos + self.directions[direction_name]

        future_bullet = Bullet(new_pos, self.entity.angle_dict[direction_name][0], False)
        collides = [
            CollideManager.checkCollide(future_bullet, obstacle)
            for obstacle in obstacles
        ]
        collides += [
            CollideManager.checkCollide(future_bullet, hud_rect)
            for hud_rect in hud
        ]
        collides += [
            CollideManager.checkCollideEntities(future_bullet, entity)
            for entity in entities
        ]

        if not any(collides):
            self.entity.pos = new_pos
        else:
            self.entity.kill()

    def move(self, obstacles, entities, hud):
        if self.entity.direction == 0:
            self.move_entity("up", obstacles, entities, hud)
        if self.entity.direction == 90:
            self.move_entity("right", obstacles, entities, hud)
        if self.entity.direction == 180:
            self.move_entity("down", obstacles, entities, hud)
        if self.entity.direction == 270:
            self.move_entity("left", obstacles, entities, hud)

class NoMovement(Move_Strategy):
    def move(self, obstacles, entities, hud):
        pass