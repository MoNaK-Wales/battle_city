from set_sprites import *
class Bullet(Entity):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.image.load('bullet.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        self.speed = 10

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.x < 0 or self.rect.x > 800:
            self.kill()