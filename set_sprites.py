import pygame
import constants
# import bullet
from abc import ABC, abstractmethod
from logger import logger


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, pos, src):
        super().__init__()

        self.pos = pygame.Vector2(pos)
        self.image = pygame.transform.scale_by(
            pygame.image.load(src), constants.SC_SCALE
        ).convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        self.rect.center = self.pos


class Entity(GameSprite):
    def __init__(self, pos, src, strategy, speed):
        super().__init__(pos, src)

        self.speed = constants.SPEED * speed * constants.SC_SCALE
        self.strategy = strategy(self)

        self.angle = 0
        self.angle_dict = {
            "up": (0, False),
            "right": (90, False),
            "down": (180, True),
            "left": (270, True),
            0: (0, False),
            90: (90, False),
            180: (180, True),
            270: (270, True),
        }
        self.is_mirrored = False  # при нижнем и правом положении спрайт отзеркален

    def move(self, obstacles, entities, hud):
        self.strategy.move(obstacles, entities, hud)

    def rotate(self, angle, to_return=False):
        logger.debug(f"Rotating {angle} {self}")
        target_angle, target_mirror = self.angle_dict[angle]
        delta_angle = target_angle - self.angle
        self.angle = target_angle
        logger.debug(f"Target angle - {target_angle}; delta - {delta_angle}")

        self.image = pygame.transform.rotate(self.image, -delta_angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.is_mirrored != target_mirror:
            logger.debug("Sprite must be mirrored")
            if target_angle == 180 or target_angle == 0:
                self.image = pygame.transform.flip(self.image, True, False)
            elif target_angle == 270 or target_angle == 90:
                self.image = pygame.transform.flip(self.image, False, True)

            self.is_mirrored = target_mirror


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
    def __init__(self, pos, stage_scene):
        super().__init__(pos, "assets/blocks/base.png")
        self.dead_image = pygame.transform.scale_by(
            pygame.image.load("assets/blocks/base_gm_over.png"), constants.SC_SCALE
        ).convert_alpha()
        self.stage_scene = stage_scene

    def destroy(self):
        logger.info("Base destroyed")
        self.image = self.dead_image
        self.rect = self.image.get_rect(center=self.pos)
        self.update()
        self.stage_scene.game_over()


class AddableGroup(pygame.sprite.Group):
    def __add__(self, other):
        if isinstance(other, pygame.sprite.Group):
            copy = self.copy()
            copy.add(other.sprites())
            return copy
        else:
            logger.error(f"Can't add {type(other)} to AddableGroup")
            return copy
