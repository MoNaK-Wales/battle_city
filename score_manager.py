import pygame
import pickle
import os
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

    high_score_path = "saves/high score.dat"

    @staticmethod
    def render(color):
        text = f"I- {ScoreManager.score:05d} HI- {ScoreManager.high_score:05d}"
        ScoreManager.score_text = ScoreManager.font.render(text, True, color, None)
        ScoreManager.score_text_rect = ScoreManager.score_text.get_rect()
        ScoreManager.score_text_rect.midtop = (SC_X_OBJ // 2, 5 * SC_SCALE)
        
        return ScoreManager.score_text, ScoreManager.score_text_rect
    
    @staticmethod
    def add(type):
        ScoreManager.score += ScoreManager.scores_dict[type]
        if ScoreManager.high_score < ScoreManager.score:
            ScoreManager.high_score = ScoreManager.score

    @staticmethod
    def clear_score():
        ScoreManager.score = 0

    @staticmethod
    def save_high_score():
        with open(ScoreManager.high_score_path, "wb") as file:
            pickle.dump(ScoreManager.high_score, file)

    @staticmethod
    def load_high_score():
        if not os.path.exists(ScoreManager.high_score_path):
            with open(ScoreManager.high_score_path, "wb") as file:
                pass

        if os.path.getsize(ScoreManager.high_score_path) > 0:
            with open(ScoreManager.high_score_path, "rb") as file:
                    ScoreManager.high_score = pickle.load(file)
        else:
            ScoreManager.high_score = 0
            ScoreManager.save_high_score()