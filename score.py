import pygame.font
from pygame.sprite import Group

class Scores():
    """Вивід ігрової інформації"""
    def __init__(self, screen, stats, enemies):
        """Ініціалізація підрахунку очок"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats
        self.enemies = enemies
        self.text_color = (139, 195, 74)
        self.font = pygame.font.SysFont(None, 36)
        self.image_score()
        self.image_high_score()

    def image_score(self):
        """Перетворення тексту рахунку в графічне зображення"""
        self.score_img = self.font.render(f"Score: {self.stats.score}", True, self.text_color, (0, 0, 0))
        self.score_rect = self.score_img.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def image_high_score(self):
        """Перетворення рекорду в графічне зображення"""
        self.high_score_image = self.font.render(f"High Score: {self.stats.high_score}", True, self.text_color, (0, 0, 0))
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top + 20

    def update(self):
        """Оновлення рахунку при вбивстві ворога"""
        for enemy in self.enemies.copy():
            if not enemy.alive():
                self.stats.score += 1
                self.enemies.remove(enemy)
                self.image_score()

    def show_score(self):
        """Відображення рахунку та рекорду на екрані"""
        self.screen.blit(self.score_img, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
