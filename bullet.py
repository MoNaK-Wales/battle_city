import constants
import strategies
from set_sprites import Entity
from sounds_manager import SoundsManager
from explosion import Explosion


class Bullet(Entity):
    def __init__(self, pos, direction, is_real = False, expl_group = None, speed = 2):
        super().__init__( pos, "assets/sprites/bullet.png", strategies.Bullet_strategy, speed)
        
        self.expl_group = expl_group
        self.speed = speed * constants.SPEED_BULLET * constants.SC_SCALE
        self.strategy = strategies.Bullet_strategy(self)
        self.direction = direction
        self.is_real = is_real
        if is_real:
            self.rotate(self.direction)
            SoundsManager.bullet_init()

    def update(self, obstacles, entities, hud):
        self.move(obstacles, entities, hud)
        self.rect.center = self.pos

    def kill(self):
        if self.is_real:
            Explosion(self.pos, "small", self.expl_group)
        super().kill()
