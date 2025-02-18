import pygame
import constants
from abc import ABC, abstractmethod

# Ініціалізація модуля mixer
pygame.mixer.init()

# Завантаження звукового файлу
saund_running = pygame.mixer.Sound("assets\sounds\Battle City SFX (16).wav")

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
        }
        self.is_mirrored = False  # при нижнем и правом положении спрайт отзеркален

    def move(self, obstacles):
        initial_pos = self.pos.copy()
        self.strategy.move(obstacles)
        if self.pos != initial_pos:
            if not pygame.mixer.get_busy():
                saund_running.play(-1)  # Відтворювати звук у циклі
        else:
            saund_running.stop()

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


class Brick(Obstacle):
    def __init__(self, pos):
        super().__init__(pos, "assets/blocks/brick.png")

    # ДОБАВИТЬ после пуль
    # def destroy():
    #     pass


class Wall(Obstacle):
    def __init__(self, pos):
        super().__init__(pos, "assets/blocks/wall.png")

class Foliage(Obstacle):
    def __init__(self, pos):
        super().__init__(pos, "assets/blocks/foliage.png")

class Base(Obstacle):
    def __init__(self, pos):
        super().__init__(pos, "assets/blocks/base.png")

    # ДОБАВИТЬ смерть после пуль


class CollideManager:
    @staticmethod
    def checkCollide(entity, obstacle):
        if not (isinstance(entity, Entity) and isinstance(obstacle, (Obstacle, pygame.Rect))):
            constants.logger.critical(f"checkCollide takes Entity and Obstacle/Rect, but {type(entity)} and {type(obstacle)} are given")
            raise TypeError("First arg must be Entity, the second one must be Obstacle (or just Rect for HUD)")

        if isinstance(obstacle, (pygame.Rect, Wall, Brick)):
            collide = entity.rect.colliderect(obstacle)
            # if isinstance(entity, Bullet), isinstance(obstacle, Wall):
            #     obstacle.destroy()
            return collide
        elif isinstance(obstacle, Foliage):
            return False

        # if isinstance(entity, Hero): #or isinstance(entity, Enemy)
        #     return True
        # elif isinstance(entity, Bullet):
        #     if isinstance(obstacle, Water):
        #         return False
        #     elif isinstance(obstacle, Brick):
        #         obstacle.destroy()
        #         return True
        #     else:
        #         return True

        constants.logger.error("Not correct Entity object was given, returning False")
        return False
    
    @staticmethod
    def checkCollideEntities(entity1, entity2):
        if not (isinstance(entity1, Entity) and isinstance(entity2, Entity)):
            constants.logger.critical(f"checkCollideEntities takes 2 Entity objects, but {type(entity1)} and {type(entity2)} are given")
            raise TypeError("Both args must be Entity")
        
        collide = entity1.rect.colliderect(entity2)
        return collide

class Move_Strategy(ABC):
    def __init__(self, entity):
        if not isinstance(entity, Entity):
            raise TypeError("Not an Entity")

        self.entity = entity
        self.speed = self.entity.speed

        self.directions = {
            "down": (0, self.speed),
            "right": (self.speed, 0),
            "up": (0, -self.speed),
            "left": (-self.speed, 0),
        }

    @abstractmethod
    def move(self, obstacles):
        pass

class Controll_Strategy(Move_Strategy):
    def move_player(self, direction_name, obstacles):
        new_pos = self.entity.pos + self.directions[direction_name]

        collides = []
        for obstacle in obstacles:
            collides.append(CollideManager.checkCollide(Hero(new_pos), obstacle))

        if not any(collides):
            self.entity.pos = new_pos
            
        self.entity.rotate(direction_name)

    def move(self, obstacles):
        keys = pygame.key.get_pressed()

        # рух гравця по клавішам
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move_player("up", obstacles)
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move_player("down", obstacles)
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.move_player("left", obstacles)
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.move_player("right", obstacles)

        # стрільба
        if keys[pygame.K_SPACE] or keys[pygame.K_x]:
            self.shoot()

    def shoot(self):
        direction = self.entity.direction
        x, y = self.entity.rect.center
        bullet = Bullet(x, y, direction)
        bullets.add(bullet)

class Bullet(Entity):
    def __init__(self, x, y, direction):
        super().__init__((x, y), 8, 8, "assets/misc/bullet.png", None, 10)
        self.direction = direction

    def update(self):
        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed

        if self.rect.x < 0 or self.rect.x > 800 or self.rect.y < 0 or self.rect.y > 600:
            self.kill()