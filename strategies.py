import pygame 
import pygame.math
from battle_city.settings import *
from abc import ABC, abstractmethod



class Move_Strategy(ABC):
    def __init__(self, move, entity):
        self.move = move
        self.entity = entity
    
    @abstractmethod
    def move(self):
        pass
class Controll_Strategy(Move_Strategy):
    def __init__(self, move, entity):
        super().__init__(move, entity)
        
        
    def move(self):
        keys = pygame.key.get_pressed()
        entity_pos = self.entity.pos
        
        # добавити паузу!!!!!!!!
        if keys[pygame.K_ESCAPE] or keys[pygame.K_KP_ENTER]:
            global Pause
            Pause = True
            
        
        
        #рух гравця по клавішам 
        if keys[pygame.K_W] or keys[pygame.K_UP]:
            entity_pos = entity_pos.move_towards(player_move_up)
            
        if keys[pygame.K_S] or keys[pygame.K_DOWN]:
            entity_pos = entity_pos.move_towards(player_move_down)
                        
        if keys[pygame.K_A] or keys[pygame.K_LEFT]:
            entity_pos = entity_pos.move_towards(player_move_left)
                    
        if keys[pygame.K_W] or keys[pygame.K_RIGHT]:
            entity_pos = entity_pos.move_towards(player_move_right)
            
            
        # стрільба
        if keys[pygame.MOUSEBUTTONDOWN] or keys[pygame.K_X]:
            # Summon_Bullet(pos ...)
            
            # ДОБАВТЕ ПУЛИ!!!
            
            # добавьте Пулю!!!
            pass
            
            
            
                    
        