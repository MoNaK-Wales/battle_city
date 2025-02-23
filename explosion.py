import pygame
import time
from constants import SC_SCALE, TANK_SCALE
from logger import logger


class Explosion(pygame.sprite.Sprite):
    anim_paths = [
        "assets/anims/explosion/expl_1.png",
        "assets/anims/explosion/expl_2.png",
        "assets/anims/explosion/expl_3.png",
        "assets/anims/explosion/expl_4.png",
        "assets/anims/explosion/expl_5.png",
    ]
    type_dict = {
        "small": 3,
        "big": 5,
    }

    def __init__(self, pos, type, group):
        super().__init__(group)

        self.pos = pos
        self.anims = [
            pygame.transform.scale_by(pygame.image.load(anim), SC_SCALE * TANK_SCALE)
            for anim in self.anim_paths
        ]

        self.lastanim = 0
        self.delay = 0.07

        self.type = self.type_dict.get(type)
        self.anims = self.anims[: self.type]
        self.anims_iter = iter(self.anims)

        if self.type is None:
            logger.error(f"Invalid explosion type: {type}")

    def update(self):
        if time.time() - self.lastanim > self.delay:
            image = next(self.anims_iter, None)
            if image is not None:
                self.image = image
                self.rect = self.image.get_rect()
                self.rect.center = self.pos
                self.lastanim = time.time()
            else:
                self.kill()
                del self
