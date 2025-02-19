import constants
import strategies
from set_sprites import Entity


class Bullet(Entity):
    def __init__(self, pos, direction, speed = 2):
        super().__init__( pos, "assets/sprites/bullet.png", strategies.Bullet_strategy, speed)
        
        self.speed = speed * constants.SPEED_BULLET * constants.SC_SCALE
        self.strategy = strategies.Bullet_strategy(self)
        self.direction = direction

    def update(self, obstacles, entitys, enemy):
        self.rect.center = self.pos
        self.move(obstacles, entitys, enemy)

    def kill(self):
        # anim.play
        super().kill()
