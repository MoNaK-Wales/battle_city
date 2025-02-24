import pygame
import sys
from abc import ABC, abstractmethod
from constants import *
from managers.logger import logger


class SceneBase(ABC):

    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager

    @abstractmethod
    def setup(self):  # перед загрузкой сцены
        pass

    @abstractmethod
    def handle_event(self, event):
        pass

    @abstractmethod
    def update(self):  # обробатывает данные каждый цикл
        pass

    @abstractmethod
    def render(self):  # прорисовывает обновлённые данные каждый цикл
        pass

    @abstractmethod
    def cleanup(self):  # перед переключением сцены на другую
        pass


class SceneManager:
    def __init__(self, screen):
        self.screen = screen
        self.scenes = {}
        self.current_scene = None

    def add_scene(self, scene_name, scene):
        if isinstance(scene, SceneBase):
            self.scenes[scene_name] = scene
            logger.info(f"{scene_name} scene added to SceneManager")

    def switch_scene(self, scene_name):
        logger.info(f"Switching from {self.current_scene} to {scene_name}")

        if self.current_scene is not None:
            self.current_scene.cleanup()

        self.current_scene = self.scenes.get(scene_name)

        if self.current_scene is not None:
            logger.info(f"Successful switching")
            self.current_scene.setup()
        else:
            logger.warning(f"Scenes dict doesn't include {scene_name} key")
            print("Name is not found")

    def run_current_scene(self):
        if self.current_scene is not None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    logger.info("Quitting the game")
                    pygame.quit()
                    sys.exit()
                self.current_scene.handle_event(event)

            self.current_scene.update()
            self.current_scene.render()
