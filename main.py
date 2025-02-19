import pygame
from pygame.sprite import Group
from scenes import *
from constants import *
from logger import logger
from score import Scores
from tanks import Enemy, SimpleEnemy

def run_game():
    global screen
    pygame.init()
    screen = pygame.display.set_mode(SC_SIZE)
    pygame.display.set_caption("Battle City")

    clock = pygame.time.Clock()

    scene_manager = SceneManager(screen)
    menu = Menu(screen, scene_manager)
    stage1 = StageLoader(screen, scene_manager, 1)
    scene_manager.add_scene("Menu", menu)
    scene_manager.add_scene("StageLoader 1", stage1)
    scene_manager.switch_scene("Menu")

    # Ініціалізація статистики та рахунку
    stats = Stats()
    enemies = Group()
    bullets = Group()
    scores = Scores(screen, stats, enemies)

    # Додавання ворогів до групи enemies
    enemy1 = SimpleEnemy(pygame.Vector2(100, 100))
    enemy2 = SimpleEnemy(pygame.Vector2(200, 200))
    enemies.add(enemy1, enemy2)

    logger.info("Run game")
    logger.debug(f"Screen: {screen}")
    logger.debug(f"Scenes list: {scene_manager.scenes}")
    logger.info("Starting loop")

    while True:
        clock.tick(FPS)

        scene_manager.run_current_scene()

        # Оновлення та відображення рахунку
        for bullet in bullets:  # Ітеруємось по всіх кулях
            hit_enemy = pygame.sprite.spritecollideany(bullet, enemies)
            if hit_enemy:
                hit_enemy.kill()
                bullet.kill()
                stats.score += 1
                scores.update()  # Оновлюємо відображення рахунку!
                break # Виходимо з циклу по кулям після зіткнення

        scores.show_score() # Виводимо рахунок на екран

        pygame.display.flip()

class Stats:
    """Клас для зберігання статистики гри"""
    def __init__(self):
        self.reset_stats()
        self.high_score = 0

    def reset_stats(self):
        self.score = 0
        self.heroes_left = 3
        self.enemies_left = 0

if __name__ == "__main__":
    run_game()