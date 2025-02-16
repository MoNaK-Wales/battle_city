import pygame 
import pygame.math
import set_sprites
from abc import ABC, abstractmethod
from constants import *


class Move_Strategy(ABC):
    def __init__(self, entity):
        if not isinstance(entity, set_sprites.Entity):
            raise TypeError("Not an Entity")
        
        self.entity = entity
        self.speed = self.entity.speed

        self.directions = {"down": (0, self.speed), "right": (self.speed, 0), "up": (0, -self.speed), "left": (-self.speed, 0)}
    
    @abstractmethod
    def move(self):
        pass

class Controll_Strategy(Move_Strategy):
    def move_player(self, direction_name):
        self.entity.pos += self.directions[direction_name]
        self.entity.rotate(direction_name)


    def move(self):
        keys = pygame.key.get_pressed()
        
        # добавити паузу!!!!!!!!
        if keys[pygame.K_ESCAPE] or keys[pygame.K_KP_ENTER]:
            global Pause
            Pause = True
            
        
        #рух гравця по клавішам 
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move_player("up")
            
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move_player("down")
                        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.move_player("left")
                    
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.move_player("right")
            
            
        # стрільба
        if keys[pygame.MOUSEBUTTONDOWN] or keys[pygame.K_x]:
            # Summon_Bullet(pos ...)
            
            # ДОБАВТЕ ПУЛИ!!!
            
            # добавьте Пулю!!!
            pass
            
            
            
                    
        