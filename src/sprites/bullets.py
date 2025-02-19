import src.constants as constants
import src.strategies.strategies as strategies
from src.sprites.game_sprites_parents import Entity

class Bullet(Entity):
    def __init__(self, pos, direction, speed = 2):
        speed *= constants.speed_bullet * constants.sc_scale
        super().__init__( pos, "assets/sprites/bullet.png", strategies.Bullet_strategy, speed)
        self.direction = direction
        

    def update(self, obstacles, entitys, enemy):
        self.rect.center = self.pos
        self.move(obstacles, entitys, enemy)
    
    def kill(self):
        # anim.play
        super().kill()