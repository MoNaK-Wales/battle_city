import pygame
import constants
from sprites.anims import Explosion
from sprites.set_sprites import GameSprite
from managers.logger import logger
from managers.sounds_manager import SoundsManager

class Obstacle(GameSprite):
    def __init__(self, pos, src):
        super().__init__(pos, src)
        logger.debug(f"Created {type(self)} obstacle on {pos}")


class Brick(Obstacle):
    def __init__(self, pos):
        super().__init__(pos, "assets/blocks/brick.png")

    def destroy(self):
        self.kill()


class Wall(Obstacle):
    def __init__(self, pos):
        super().__init__(pos, "assets/blocks/wall.png")

class Foliage(Obstacle):
    def __init__(self, pos):
        super().__init__(pos, "assets/blocks/foliage.png")

class Base(Obstacle):

    def __init__(self, pos, stage_scene, expl_group):
        super().__init__(pos, "assets/blocks/base.png")
        self.dead_image = pygame.transform.scale_by(
            pygame.image.load("assets/blocks/base_gm_over.png"), constants.SC_SCALE
        ).convert_alpha()
        self.stage_scene = stage_scene
        self.expl_group = expl_group

    def destroy(self):
        logger.info("Base destroyed")
        self.image = self.dead_image
        self.rect = self.image.get_rect(center=self.pos)
        self.update()

        Explosion(self.pos, "big", self.expl_group)
        SoundsManager.player_destroyed()
        self.stage_scene.game_over()
