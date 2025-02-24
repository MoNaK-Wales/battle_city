import pygame
import time
from constants import *
from scenes.base_scenes import SceneBase
from scenes.stage import Stage
from managers.logger import logger
from managers.sounds_manager import SoundsManager


class StageLoader(SceneBase):
    def __init__(self, screen, scene_manager, level):
        super().__init__(screen, scene_manager)

        self.background_color = GREY
        self.level = level

        self.stage_font = pygame.font.Font(NES_FONT, FONT_SIZE * SC_SCALE)
        self.stage_text = self.stage_font.render(
            f"STAGE {self.level}", False, BLACK, GREY
        )
        self.stage_text_rect = self.stage_text.get_rect()
        self.stage_text_rect.center = (SC_X_OBJ / 2, SC_Y_OBJ / 2)

    def setup(self):
        logger.info("StageLoader setup")
        self.screen.fill(self.background_color)
        self.screen.blit(self.stage_text, self.stage_text_rect)
        pygame.display.flip()
        SoundsManager.pause(True)
        SoundsManager.pause(False)
        SoundsManager.startlevel()
        time.sleep(3)
        next_scene = Stage(self.screen, self.scene_manager, self.level)
        self.scene_manager.add_scene(f"Stage {self.level}", next_scene)
        self.scene_manager.switch_scene(f"Stage {self.level}")

    def update(self):
        pass

    def render(self):
        pass

    def handle_event(self, event):
        pass

    def cleanup(self):
        logger.info("StageLoader cleanup")
