import pygame
import pygame.math
import set_sprites
from abc import ABC, abstractmethod
from constants import *


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

    @abstractmethod
    def move(self, obstacles):
        pass


class Controll_Strategy(Move_Strategy):
    def move_player(self, direction_name, obstacles):
        new_pos = self.entity.pos + self.directions[direction_name]
        
        future_hero = set_sprites.Hero(new_pos)
        collides = [set_sprites.CollideManager.checkCollide(future_hero, obstacle) for obstacle in obstacles]

        if not any(collides):
            self.entity.pos = new_pos
        if self.entity.angle != self.entity.angle_dict[direction_name][0]:
            self.entity.rotate(direction_name)

    def move(self, obstacles):
        keys = pygame.key.get_pressed()

        # добавити паузу!!!!!!!!
        if keys[pygame.K_ESCAPE] or keys[pygame.K_KP_ENTER]:
            logger.info("Pause")
            global Pause
            Pause = True

        # рух гравця по клавішам
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move_player("up", obstacles)
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move_player("down", obstacles)
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.move_player("left", obstacles)
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.move_player("right", obstacles)

        # стрільба
        if keys[pygame.MOUSEBUTTONDOWN] or keys[pygame.K_x]:
            # Summon_Bullet(pos ...)

            # ДОБАВТЕ ПУЛИ!!!

            # добавьте Пулю!!!
            pass


class Enemy_Strategy(Move_Strategy):
    def move(self, obstacles):
        print("moving")