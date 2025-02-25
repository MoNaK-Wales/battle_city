import pygame
import time
from constants import SC_SCALE, TANK_SCALE
from logger import logger


class Animation(pygame.sprite.Sprite):
    def __init__(self, pos, group, end_func, delay, anims_iter):
        super().__init__(group)

        self.pos = pos
        self.end_func = end_func
        self.lastanim = 0
        self.delay = delay
        self.anims_iter = anims_iter

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
                if self.end_func is not None:
                    self.end_func()
                del self


class Explosion(Animation):
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

    def __init__(self, pos, type, group, end_func = None):
        self.anims = [
            pygame.transform.scale_by(pygame.image.load(anim), SC_SCALE * TANK_SCALE)
            for anim in self.anim_paths
        ]

        self.type = self.type_dict.get(type)
        self.anims = self.anims[: self.type]
        self.anims_iter = iter(self.anims)

        if self.type is None:
            logger.error(f"Invalid explosion type: {type}")

        super().__init__(pos, group, end_func, 0.07, self.anims_iter)


class SpawnAnim(Animation):
    anim_paths = [
        "assets/anims/spawn/spawn1.png",
        "assets/anims/spawn/spawn2.png",
        "assets/anims/spawn/spawn3.png",
        "assets/anims/spawn/spawn4.png",
    ]

    def __init__(self, pos, group, end_func):
        self.anims = [
            pygame.transform.scale_by(pygame.image.load(anim), SC_SCALE)
            for anim in self.anim_paths
        ]
        self.anims_iter = iter(self.anims[::-1] * 2) # анимация спавна от самого большого до маленького 2 раза

        super().__init__(pos, group, end_func, 0.1, self.anims_iter)