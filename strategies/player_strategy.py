import pygame
import strategies.base_strategy
from sprites.bullet import Bullet
from time import *

class ControllStrategy(strategies.base_strategy.MoveStrategy):
    def move(self):
        keys = pygame.key.get_pressed()

        # рух гравця по клавішам
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move_entity("up")
            self.entity.anim()
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move_entity("down")
            self.entity.anim()
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.move_entity("left")
            self.entity.anim()
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.move_entity("right")
            self.entity.anim()

        # стрільба
        if (keys[pygame.MOUSEBUTTONDOWN] or keys[pygame.K_x]) and time() - self.last_shot > 0.85:
            bullet_pos = pygame.Vector2(self.entity.rect.center) + pygame.Vector2(self.bullet_pos[self.entity.angle])
            Bullet(bullet_pos, self.entity.angle, True, self.bullets, self.anims, 2)
            self.last_shot = time()