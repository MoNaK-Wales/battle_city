import pygame
import src.constants as constants
from src.sprites.game_sprites_parents import Entity, Obstacle
from src.sprites.obstacles import Wall, Brick, Foliage

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