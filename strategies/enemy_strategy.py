import random
import pygame
import strategies.base_strategy
from sprites.bullet import Bullet
from constants import *

class EnemyStrategy(strategies.base_strategy.MoveStrategy):
    # легкий 7/8 - случайно идёт, 1/8 - идёт к базе --- обычный танк
    # normal 1/8 - идет к базе, 1/4 - случайно идет, 5/8 - идёт к игроку --- сильный и брониndom.randint танк
    # hard 2/7 - идёт к базе, 1/7 - случайно идёт, 4/7 - идёт к игроку --- быстрый
    # все танки меняют направление раз в 0.5 секунд, стреляют раз в 4/3 секунд (сильный - раз в 2/3)

    def __init__(self, entity, obstacles, entities, hud, bullets, anims):
        super().__init__(entity, obstacles, entities, hud, bullets, anims)

        self.move_timer = -1  # Счётчик кадров
        self.move_delay = FPS * 0.3
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
        baseX, baseY = 116 * SC_SCALE, 212 * SC_SCALE
        self.x, self.y = self.entity.pos

        if self.y < baseY and random.randint(1, 5) != 5:
            pos = "down"
        elif self.x > baseX:
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