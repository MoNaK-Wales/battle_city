import pygame
import time
import constants
from itertools import cycle


class Explosion(pygame.sprite.Sprite):
    anim1 = "assets/anims/explosion/expl_1.png"
    anim2 = "assets/anims/explosion/expl_2.png"
    anim3 = "assets/anims/explosion/expl_3.png"
    anim4 = "assets/anims/explosion/expl_4.png"
    anim5 = "assets/anims/explosion/expl_5.png"

    def __init__(self, pos):
        self.pos = pos
        self.anims = [self.anim1, self.anim2, self.anim3, self.anim4, self.anim5]
        self.lastanim = 0

    def small_explosion(self):
        for anim in self.anims[:3]:
            next = False
            while not next:
                if time.time() - self.lastanim > 0.05:
                    self.image = pygame.transform.scale_by(pygame.image.load(anim), constants.SC_SCALE)
                    self.lastanim = time.time()
                    self.rect = self.image.get_rect()
                    self.rect.center = self.pos
                    pygame.display.get_surface().blit(self.image, self.rect)
                    pygame.display.flip()
                    next = True