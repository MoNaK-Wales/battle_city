import pygame
from scenes import *
from constants import *


def run_game():
    pygame.init()
    screen = pygame.display.set_mode(sc_size)
    pygame.display.set_caption("Battle City")
    clock = pygame.time.Clock()

    scene_manager = SceneManager(screen)
    menu = Menu(screen, scene_manager)
    stage1 = Stage(screen, scene_manager, "assets/stages/")
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

        pygame.display.flip()


if __name__ == "__main__":
    run_game()