import pygame
from constants import *


class ScoreManager:
    pygame.font.init()

    scores_dict = {
        "Simple": 100,
        "Fast": 200,
        "Power": 300,
        "Armor": 400,
        "Bonus": 500,
    }
    font = pygame.font.Font(NES_FONT, MINI_FONT_SIZE * SC_SCALE)
    #  "I- 00000 HI- 00000"

    score = 0
    high_score = 0

    @staticmethod
    def render(color):
        text = f"I- {ScoreManager.score:05d} HI- {ScoreManager.high_score:05d}"
        ScoreManager.score_text = ScoreManager.font.render(text, True, color, None)
        ScoreManager.score_text_rect = ScoreManager.score_text.get_rect()
        ScoreManager.score_text_rect.midtop = (SC_X_OBJ // 2, 5 * SC_SCALE)
        
        return ScoreManager.score_text, ScoreManager.score_text_rect
    
    # @staticmethod
    # def add():
    #     ScoreManager.score