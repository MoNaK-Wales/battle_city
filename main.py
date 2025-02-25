import pygame
from pygame.sprite import Group
from scenes import *
from constants import *
from logger import logger
from Score import Score
from Stats import Score
from tanks import Hero

def run_game():
    global screen
    pygame.init()
    screen = pygame.display.set_mode(SC_SIZE)
    pygame.display.set_caption("Battle City")

    clock = pygame.time.Clock()

    # Ініціалізація статистики та рахунку
    stats = Stats()
    enemies = Group()
    bullets = Group()
    score = Score()

    scene_manager = SceneManager(screen)
    menu = Menu(screen, scene_manager)
    stage1 = StageLoader(screen, scene_manager, 1)
    
    # Передаємо групи в StageLoader
    stage1.enemies = enemies
    stage1.bullets = bullets
    
    scene_manager.add_scene("Menu", menu)
    scene_manager.add_scene("StageLoader 1", stage1)
    scene_manager.switch_scene("Menu")

    logger.info("Run game")
    logger.debug(f"Screen: {screen}")
    logger.debug(f"Scenes list: {scene_manager.scenes}")
    logger.info("Starting loop")

    while True:
        clock.tick(FPS)
        
        scene_manager.run_current_scene()

        # Перевірка зіткнень куль з ворогами
        for bullet in bullets.sprites():  # Використовуємо sprites() для безпечної ітерації
            hits = pygame.sprite.spritecollide(bullet, enemies, False)  # False щоб не видаляти ворога автоматично
            if hits:
                bullet.kill()  # Видаляємо кулю
                for hit in hits:
                    hit.kill()  # Видаляємо ворога
                    score.add(1)  # Збільшуємо рахунок
                    logger.info(f"Score increased: {score.get()}")  # Логування зміни

        # Оновлення груп
        enemies.update()
        bullets.update()
        
        # Відображення рахунку
        # (Додайте код для відображення рахунку на екрані, якщо потрібно)
        
        if DRAW_GRID:
            drawGrid()

        pygame.display.flip()

def drawGrid():
    blockSize = 24
    for x in range(0, SC_X_OBJ, blockSize):
        for y in range(0, SC_Y_OBJ, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)

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
