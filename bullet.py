import constants
import strategies
from set_sprites import Entity


class Bullet(Entity):
    def __init__(self, pos, direction, is_real = True, speed = 2):
        super().__init__( pos, "assets/sprites/bullet.png", strategies.Bullet_strategy, speed)
        
        self.speed = speed * constants.SPEED_BULLET * constants.SC_SCALE
        self.strategy = strategies.Bullet_strategy(self)
        self.direction = direction
        if is_real:
            self.rotate(self.direction)

    def update(self, obstacles, entities, hud):
        self.move(obstacles, entities, hud)
        self.rect.center = self.pos

    def kill(self):
        # anim.play
        super().kill()
