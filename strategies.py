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
    # легкий 7/8 - случайно идёт, 1/8 - идёт к базе --- обычный танк
    # normal 1/8 - идет к базе, 1/4 - случайно идет, 5/8 - идёт к игроку --- сильный и брониndom.randint танк
    # hard 2/7 - идёт к базе, 1/7 - случайно идёт, 4/7 - идёт к игроку --- быстрый
    # все танки меняют направление раз в 0.5 секунд, стреляют раз в 4/3 секунд (сильный - раз в 2/3)

    def __init__(self, entity, obstacles, entities, hud, bullets, anims):
        super().__init__(entity, obstacles, entities, hud, bullets, anims)

        self.move_timer = -1  # Счётчик кадров
        self.move_delay = FPS * 0.5
        self.shoot_delay = entity.shoot_delay * 1.3
        self.direction_keys = list(self.directions.keys())
        self.random_direction = random.choice(self.direction_keys)

    def move(self):
        pass

    def fire(self):
        if self.last_shot >= self.shoot_delay and random.randint(1, 10) < 8:        # 70%
            bullet_pos = pygame.Vector2(self.entity.rect.center) + pygame.Vector2(self.bullet_pos[self.entity.angle])
            Bullet(bullet_pos, self.entity.angle, True, self.bullets, self.anims, 2, True)
            self.last_shot = 0
        else:
            self.last_shot += 1

    def random_pos(self):
        return random.choice(self.direction_keys)
    
    def to_player_pos(self):
        hero = self.entity.find_hero(self.entities)
        if hero is None:
            return self.to_base_pos()

        heroX, heroY = hero.pos
        self.x, self.y = self.entity.pos

        if random.choice([True, False]):  #случайно выбирается ось
            if self.x > heroX:
                pos = "left"
            else:
                pos = "right"
        else:
            if self.y > heroY:
                pos = "up"
            else:
                pos = "down"
        
        return pos
    
    def to_base_pos(self):
        baseX = 116 * SC_SCALE
        self.x, self.y = self.entity.pos

        if self.x > baseX:
            pos = "left"
        elif self.x < baseX:
            pos = "right"
        else:
            pos = "down"

        return pos
        

class EnemyEasyStrategy(EnemyStrategy):    
    def move(self):
        if self.move_timer >= self.move_delay or self.move_timer == -1:
            random_int = random.randint(1, 8)
            if random_int == 8:
                self.direction = self.to_base_pos()
            else:
                self.direction = self.random_pos()
            self.move_timer = 0
        else:
            self.move_timer += 1
        
        self.move_entity(self.direction)
        self.fire()
        self.entity.anim()


class EnemyNormalStrategy(EnemyStrategy):
    def move(self):
        if self.move_timer >= self.move_delay or self.move_timer == -1:
            random_int = random.randint(1, 8)
            if random_int <= 5:
                self.direction = self.to_player_pos()
            elif random_int in (6, 7):
                self.direction = self.random_pos()
            elif random_int == 8:
                self.direction = self.to_base_pos()
            self.move_timer = 0
        else:
            self.move_timer += 1
            
        self.move_entity(self.direction)
        self.fire()
        self.entity.anim()
        

class EnemyHardStrategy(EnemyStrategy):
    def move(self):
        if self.move_timer >= self.move_delay or self.move_timer == -1:
            random_int = random.randint(1, 7)
            if random_int <= 4:
                self.direction = self.to_player_pos()
            elif random_int in (5, 6):
                self.direction = self.to_base_pos()
            elif random_int == 7:
                self.direction = self.random_pos()
            self.move_timer = 0
        else:
            self.move_timer += 1
            
        self.move_entity(self.direction)
        self.fire()
        self.entity.anim()


class BulletStrategy(MoveStrategy):
    def move_entity(self, direction_name):
        new_pos = self.entity.pos + self.directions[direction_name]

        future_bullet = Bullet(new_pos, self.entity.angle_dict[direction_name][0])
        future_bullet.of_enemy = self.entity.of_enemy
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
