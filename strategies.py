import pygame
import pygame.math
import set_sprites
from abc import ABC, abstractmethod
from constants import *
import random
from time import *

class Move_Strategy(ABC):
    def __init__(self, entity):
        if not isinstance(entity, set_sprites.Entity):
            raise TypeError("Not an Entity")

        self.entity = entity
        self.speed = self.entity.speed
        self.move_timer = 0  # Счётчик кадров
        self.move_delay = random.randint(10, 50)  # Случайная задержка в кадрах
        self.random_direction = random.choice(["up", "down", "left", "right"])

        self.directions = {
            "down": (0, self.speed),
            "right": (self.speed, 0),
            "up": (0, -self.speed),
            "left": (-self.speed, 0),
        }

    @abstractmethod
    def move(self, obstacles, enemy):
        pass


class Controll_Strategy(Move_Strategy):
    def move_player(self, direction_name, obstacles, entitys):
        new_pos = self.entity.pos + self.directions[direction_name]
        
        future_hero = set_sprites.Hero(new_pos)
        collides = [set_sprites.CollideManager.checkCollide(future_hero, obstacle) for obstacle in obstacles]
        collides.append(set_sprites.CollideManager.checkCollideEntities(future_hero, entitys))

        if not any(collides):
            self.entity.pos = new_pos
        if self.entity.angle != self.entity.angle_dict[direction_name][0]:
            self.entity.rotate(direction_name)

    def move(self, obstacles, entitys, enemy):
        keys = pygame.key.get_pressed()

        # добавити паузу!!!!!!!!
        if keys[pygame.K_ESCAPE] or keys[pygame.K_KP_ENTER]:
            logger.info("Pause")
            global Pause
            Pause = True

        # рух гравця по клавішам
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move_player("up", obstacles, enemy)
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move_player("down", obstacles, enemy)
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.move_player("left", obstacles, enemy)
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.move_player("right", obstacles, enemy)

        # стрільба
        # if keys[pygame.MOUSEBUTTONDOWN] or keys[pygame.K_x]:
        #     bullet = set_sprites.Bullet(self.entity.rect.center, self.entity.angle)
        #     bullet.add(bullet)

        #     # ДОБАВТЕ ПУЛИ!!!

        #     # добавьте Пулю!!!
        #     pass

        
class Enemy_Strategy(Move_Strategy):
    def move_enemy(self, direction_name, obstacles, entitys, enemy):
        new_pos = self.entity.pos + self.directions[direction_name]

        future_enemy = set_sprites.Enemy(new_pos)
        collides = [set_sprites.CollideManager.checkCollide(future_enemy, obstacle) for obstacle in obstacles]
        collides.append(set_sprites.CollideManager.checkCollideEntities(future_enemy, entitys))
        
        if not any(collides):
            self.entity.pos = new_pos
        self.entity.rotate(direction_name)
        
    # def move(self, obstacles, entitys, enemy):
    #     keys = pygame.key.get_pressed()
        


    # def move(self, obstacles, entitys, enemy):
    #     directions = ["up", "down", "left", "right"]
    #     random_direction = random.choice(directions)  # Выбираем случайное направление
    #     self.move_enemy(random_direction, obstacles, entitys, enemy)

    def move(self, obstacles, entitys, enemy):

        self.move_enemy(self.random_direction, obstacles, entitys, enemy)
        if self.move_timer >= self.move_delay:  # Проверяем, прошла ли задержка
            self.random_direction = random.choice(["up", "down", "left", "right"])  # Выбираем случайное направление
            

            # Сбрасываем таймер и задаём новую случайную задержку
            self.move_timer = 0
            self.move_delay = random.randint(10, 50)
        else:
            self.move_timer += 1
              # Увеличиваем таймер каждую итерацию игрового цикла  


            
class Bullet_strategy(Move_Strategy):
    def move_bullet(self, direction_name, obstacles, entitys, enemy):
        new_pos = self.entity.pos + self.directions[direction_name]

        future_bullet = set_sprites.Entity(new_pos)
        collides = [set_sprites.CollideManager.checkCollide(future_bullet, obstacle) for obstacle in obstacles]
        collides.append(set_sprites.CollideManager.checkCollideEntities(future_bullet, entitys))
        
        if not any(collides):
            self.entity.pos = new_pos
        self.entity.rotate(direction_name)
        
    def move(self, obstacles, entitys, enemy):
        if self.entity.angle == self.entity.angle_dict["up"][0]:
            self.move_bullet("up", obstacles, entitys, enemy)
        if self.entity.angle == self.entity.angle_dict["left"][0]:
            self.move_bullet("left", obstacles, entitys, enemy)        
        if self.entity.angle == self.entity.angle_dict["right"][0]:
            self.move_bullet("right", obstacles, entitys, enemy)
        if self.entity.angle == self.entity.angle_dict["right"][0]:
            self.move_bullet("right", obstacles, entitys, enemy)
