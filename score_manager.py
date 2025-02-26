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
        "Level": 1000,
    }
    font = pygame.font.Font(NES_FONT, MINI_FONT_SIZE * SC_SCALE)
    plus_font = pygame.font.Font(NES_FONT, MINI_FONT_SIZE * SC_SCALE)
    plus_text = ""
    #  "+100" "I- 00000 HI- 00000"

    plus_text_timer = -1

    score = 0
    high_score = 0

    given_hp_up = 0

    high_score_path = "saves/high score.dat"

    @staticmethod
    def render(color):
        text = f"I- {ScoreManager.score:05d} HI- {ScoreManager.high_score:05d}"
        score_text = ScoreManager.font.render(text, True, color, None)
        score_text_rect = score_text.get_rect()
        score_text_rect.midtop = (SC_X_OBJ // 2, 5 * SC_SCALE)

        score_plus_text = ScoreManager.plus_font.render(ScoreManager.plus_text, True, color, None)
        score_plus_text_rect = score_plus_text.get_rect()
        score_plus_text_rect.topleft = (40 * SC_SCALE, 5 * SC_SCALE)

        if ScoreManager.plus_text_timer > PLUS_TEXT_DELAY:
            ScoreManager.plus_text = ""
            ScoreManager.plus_text_timer = -1
        elif ScoreManager.plus_text_timer != -1:
            ScoreManager.plus_text_timer += 1
        
        return score_text, score_text_rect, score_plus_text, score_plus_text_rect
    
    @staticmethod
    def add(type):
        adding = ScoreManager.scores_dict[type]
        ScoreManager.score += adding
        if ScoreManager.high_score < ScoreManager.score:
            ScoreManager.high_score = ScoreManager.score

        ScoreManager.plus_text = f"{adding}À"
        ScoreManager.plus_text_timer = 0

    @staticmethod
    def clear_score():
        ScoreManager.score = 0
        ScoreManager.given_hp_up = 0

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