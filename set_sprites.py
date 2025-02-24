import pygame
import constants
from logger import logger
from anims import Explosion
from sounds_manager import SoundsManager


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
        self.strategy = strategy(self, None, None, None, None, None)

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

        self.original_image = self.image.copy()

        # при спавне существо будет считаться находящимся внутри игрока, и только после выхода из него (может сразу при спавне) 
        # флаг отключается и может проверяться коллизия
        self.is_overlap_entity = True

    def update(self, **kwargs):
        # если существо есть в группе существ, надо его удалить
        entities = kwargs["entities"].copy()
        if entities.has(self):
            entities.remove(self)

        self.strategy.obstacles = kwargs["obstacles"]
        self.strategy.entities = entities
        self.strategy.hud = kwargs["hud"]
        self.strategy.bullets = kwargs["bullets"]
        self.strategy.anims = kwargs["anims"]

        if self.is_overlap_entity:
            self.check_entity_overlapping(entities)

    def move(self):
        self.strategy.move()

    def rotate(self, angle):
        logger.debug(f"Rotating {angle} {self}")
        target_angle, target_mirror = self.angle_dict[angle]
        self.angle = target_angle

        rotated_image = pygame.transform.rotate(self.original_image, -target_angle)

        if target_mirror:
            logger.debug("Sprite must be mirrored")
            if target_angle in (0, 180):
                rotated_image = pygame.transform.flip(rotated_image, True, False)
            elif target_angle in (90, 270):
                rotated_image = pygame.transform.flip(rotated_image, False, True)

        self.image = rotated_image
        self.rect = self.image.get_rect(center=self.rect.center)

    def check_entity_overlapping(self, entities):
        collides = []
        for entity in entities:
            collides.append(not self.rect.colliderect(entity.rect))

        if all(collides):
            self.is_overlap_entity = False   


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


class AddableGroup(pygame.sprite.Group):
    def __add__(self, other):
        if isinstance(other, pygame.sprite.Group):
            copy = self.copy()
            copy.add(other.sprites())
            return copy
        else:
            logger.error(f"Can't add {type(other)} to AddableGroup")
            return copy
