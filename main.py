import pygame
from scenes import *
from constants import *
from logger import logger


def run_game():
    global screen
    pygame.init()
    screen = pygame.display.set_mode(SC_SIZE)
    pygame.display.set_caption("Battle City")

    clock = pygame.time.Clock()

    scene_manager = SceneManager(screen)
    menu = Menu(screen, scene_manager)
    stage1 = StageLoader(screen, scene_manager, 1)
    gameover = GameOver(screen, scene_manager)
    scene_manager.add_scene("Menu", menu)
    scene_manager.add_scene("StageLoader 1", stage1)
    scene_manager.add_scene("Game over", gameover)
    scene_manager.switch_scene("Menu")

    logger.info("Run game")
    logger.debug(f"Screen: {screen}")
    logger.debug(f"Scenes list: {scene_manager.scenes}")
    logger.info("Starting loop")

    while True:
        clock.tick(FPS)

        scene_manager.run_current_scene()

        if DRAW_GRID:
            drawGrid()

        pygame.display.flip()

def drawGrid():
    blockSize = 24
    for x in range(0, SC_X_OBJ, blockSize):
        for y in range(0, SC_Y_OBJ, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)


if __name__ == "__main__":
    run_game()
