import pygame
import src.constants as constants

class Game_Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, src):
        super().__init__()

        self.pos = pygame.Vector2(pos)
        self.image = pygame.transform.scale_by(pygame.image.load(src), constants.sc_scale).convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        self.rect.center = self.pos


class Entity(Game_Sprite):
    def __init__(self, pos, src, strategy, speed):
        super().__init__(pos, src)

        self.image = pygame.transform.scale_by(pygame.image.load(src), constants.sc_scale).convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)

        self.speed = constants.speed * speed * constants.sc_scale
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

    def move(self, obstacles, entitys, enemy):
        self.strategy.move(obstacles, entitys, enemy)

    def rotate(self, angle):
        constants.logger.info(f"Rotating {angle} {self}")
        target_angle, target_mirror = self.angle_dict[angle]
        delta_angle = target_angle - self.angle
        self.angle = target_angle
        constants.logger.debug(f"Target angle - {target_angle}; delta - {delta_angle}")

        self.image = pygame.transform.rotate(self.image, -delta_angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.is_mirrored != target_mirror:
            constants.logger.debug("Sprite must be mirrored")
            if target_angle == 180 or target_angle == 0:
                self.image = pygame.transform.flip(self.image, True, False)
            elif target_angle == 270 or target_angle == 90:
                self.image = pygame.transform.flip(self.image, False, True)

            self.is_mirrored = target_mirror


class Obstacle(Game_Sprite):
    def __init__(self, pos, src):
        super().__init__(pos, src)
        constants.logger.debug(f"Created {type(self)} obstacle on {pos}")