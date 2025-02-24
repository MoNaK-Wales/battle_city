from abc import ABC, abstractmethod
from managers.collide_manager import CollideManager
from sprites.set_sprites import Entity
from constants import *

class MoveStrategy(ABC):
    def __init__(self, entity, obstacles, entities, hud, bullets, anims):
        if not isinstance(entity, Entity):
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
        future_entity.is_overlap_entity = self.entity.is_overlap_entity

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


class NoMovement(MoveStrategy):
    def __init__(self):
        pass
    def move(self):
        pass
