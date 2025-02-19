import pygame
from src.scenes import *
from src.constants import *


def run_game():
    global screen
    pygame.init()
    screen = pygame.display.set_mode(sc_size)
    pygame.display.set_caption("Battle City")
    
    clock = pygame.time.Clock()
    
    scene_manager = SceneManager(screen)
    menu = Menu(screen, scene_manager)
    stage1 = Stage(screen, scene_manager, "assets/stages/stage1")
    scene_manager.add_scene("Menu", menu)
    scene_manager.add_scene("Stage 1", stage1)
    scene_manager.switch_scene("Menu")

    logger.info("Run game")
    logger.debug(f"Screen: {screen}")
    logger.debug(f"Scenes list: {scene_manager.scenes}")
    logger.info("Starting loop")

    while True:
        clock.tick(FPS)

        
        scene_manager.run_current_scene()
        drawGrid()

        pygame.display.flip()

def drawGrid():
    blockSize = 24 #Set the size of the grid block
    for x in range(0, sc_x_obj, blockSize):
        for y in range(0, sc_y_obj, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)


if __name__ == "__main__":
    run_game()