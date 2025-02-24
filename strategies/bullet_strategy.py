import strategies.base_strategy
from managers.collide_manager import CollideManager
from sprites.bullet import Bullet


class BulletStrategy(strategies.base_strategy.MoveStrategy):
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