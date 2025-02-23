import pygame
from logger import logger
from bullet import Bullet
from set_sprites import Entity, Obstacle, Wall, Brick, Foliage, Base
from sounds_manager import SoundsManager


class CollideManager:
    @staticmethod
    def checkCollide(entity, obstacle):
        if not (isinstance(entity, Entity) and isinstance(obstacle, (Obstacle, pygame.Rect))):
            logger.critical(
                f"checkCollide takes Entity and Obstacle/Rect, but {type(entity)} and {type(obstacle)} are given"
            )
            raise TypeError("First arg must be Entity, the second one must be Obstacle (or just Rect for HUD)")

        if isinstance(obstacle, (pygame.Rect, Wall, Brick, Base)):
            collide = entity.rect.colliderect(obstacle)
            if isinstance(entity, Bullet) and collide:
                if isinstance(obstacle, (Brick, Base)):
                    SoundsManager.bullet_bricks()
                    obstacle.destroy()
                if isinstance(obstacle, (Wall, pygame.Rect)):
                    SoundsManager.bullet_wall()
                entity.kill()
            return collide
        elif isinstance(obstacle, Foliage):
            return False

        logger.error("Not correct Entity object was given, returning False")
        return False

    @staticmethod
    def checkCollideEntities(entity1, entity2):
        if not (isinstance(entity1, Entity) and isinstance(entity2, Entity)):
            logger.critical(
                f"checkCollideEntities takes 2 Entity objects, but {type(entity1)} and {type(entity2)} are given"
            )
            raise TypeError("Both args must be Entity")

        collide = entity1.rect.colliderect(entity2)
        if collide and (isinstance(entity1, Bullet) or isinstance(entity2, Bullet)):
            entity1.kill()
            entity2.kill()        
        return collide
