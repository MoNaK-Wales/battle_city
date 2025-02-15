import pygame 
import pygame.math
from constants import *
from abc import ABC, abstractmethod

class Move_Strategy(ABC):
    def __init__(self, entity):
        self.entity = entity

        self.player_move_down = [0, self.entity.speed]
        self.player_move_right = [self.entity.speed, 0]
        self.player_move_up = [0, self.entity.speed]
        self.player_move_left = [self.entity.speed, 0]
    
    @abstractmethod
    def move(self):
        pass

class Controll_Strategy(Move_Strategy):        
    def move(self):
        keys = pygame.key.get_pressed()
        
        # добавити паузу!!!!!!!!
        if keys[pygame.K_ESCAPE] or keys[pygame.K_KP_ENTER]:
            global Pause
            Pause = True
            
        
        #рух гравця по клавішам 
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.entity.pos += self.player_move_up
            
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.entity.pos += self.player_move_down
                        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.entity.pos += self.player_move_left
                    
        if keys[pygame.K_w] or keys[pygame.K_RIGHT]:
            self.entity.pos += self.player_move_right
            
            
        # стрільба
        if keys[pygame.MOUSEBUTTONDOWN] or keys[pygame.K_x]:
            # Summon_Bullet(pos ...)
            
            # ДОБАВТЕ ПУЛИ!!!
            
            # добавьте Пулю!!!
            pass
            
            
            
                    
        