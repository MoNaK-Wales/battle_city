import pygame
from constants import *
from scenes.base_scenes import SceneBase
from managers.logger import logger


class Menu(SceneBase):
    def __init__(self, screen, scene_manager):
        super().__init__(screen, scene_manager)

        self.background_color = BLACK

        self.menu_font = pygame.font.Font(NES_FONT, FONT_SIZE * SC_SCALE)
        self.start_button = self.menu_font.render("START GAME", False, WHITE, BLACK)
        self.start_button_rect = self.start_button.get_rect()
        self.start_button_rect.center = (SC_X_OBJ / 2, SC_Y_OBJ * 0.8)

        self.logo = pygame.transform.scale_by(
            pygame.image.load("assets/misc/logo.png").convert(), 0.35 * SC_SCALE
        )
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.center = (SC_X_OBJ / 2, SC_Y_OBJ * 0.540)

        self.tank_logo = pygame.transform.scale_by(
            pygame.image.load("assets/misc/tank_logo.png").convert(), 0.14 * SC_SCALE
        )
        self.tank_logo_rect = self.tank_logo.get_rect()
        self.tank_logo_rect.center = (SC_X_OBJ / 2, SC_Y_OBJ * 0.2)

    def setup(self):
        logger.info("Menu setup")

        self.screen.fill(self.background_color)
        self.screen.blit(self.start_button, self.start_button_rect)
        self.screen.blit(self.logo, self.logo_rect)
        self.screen.blit(self.tank_logo, self.tank_logo_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if self.start_button_rect.collidepoint(mouse_x, mouse_y):
                logger.debug(f"LMB click on start button at {event.pos}")
                self.scene_manager.switch_scene("StageLoader 1")
        elif event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_RETURN]:  # enter
                logger.debug(f"Starting game via enter")
                self.scene_manager.switch_scene("StageLoader 1")

    def render(self):
        pass

    def update(self):
        pass

    def cleanup(self):
        logger.info("Menu cleanup")