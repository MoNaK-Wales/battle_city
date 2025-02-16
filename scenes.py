import pygame
import sys
from constants import *
from set_sprites import *
from abc import ABC, abstractmethod
from level_manager import *


class SceneBase(ABC):
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


class Menu(SceneBase):
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager

        self.background_color = black

        self.menu_font = pygame.font.Font(NES_font, font_size * sc_scale)
        self.start_button = self.menu_font.render("START GAME", False, white, black)
        self.start_button_rect = self.start_button.get_rect()
        self.start_button_rect.center = (sc_x_obj / 2, sc_y_obj * 0.8)

        self.logo = pygame.transform.scale_by(
            pygame.image.load("assets/misc/logo.png").convert(), 0.35 * sc_scale
        )
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.center = (sc_x_obj / 2, sc_y_obj * 0.540)

        self.tank_logo = pygame.transform.scale_by(
            pygame.image.load("assets/misc/tank_logo.png").convert(), 0.14 * sc_scale
        )
        self.tank_logo_rect = self.tank_logo.get_rect()
        self.tank_logo_rect.center = (sc_x_obj / 2, sc_y_obj * 0.2)

    def setup(self):
        self.screen.fill(self.background_color)
        self.screen.blit(self.start_button, self.start_button_rect)
        self.screen.blit(self.logo, self.logo_rect)
        self.screen.blit(self.tank_logo, self.tank_logo_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if self.start_button_rect.collidepoint(mouse_x, mouse_y):
                self.scene_manager.switch_scene("Stage 1")
        elif event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_RETURN]:  # enter
                self.scene_manager.switch_scene("Stage 1")

    def render(self):
        pass

    def update(self):
        pass

    def cleanup(self):
        pass


class Stage(SceneBase):
    def __init__(self, screen, scene_manager, map):
        self.screen = screen
        self.scene_manager = scene_manager
        self.map = map

        self.background_color = black

        self.top_hud = pygame.Surface((sc_x_obj, hud_width))
        self.top_hud.fill(grey)
        self.left_hud = pygame.Surface((hud_width, sc_y_obj))
        self.left_hud.fill(grey)
        self.bottom_hud = pygame.Surface((sc_x_obj, hud_width))
        self.bottom_hud.fill(grey)
        self.right_hud = pygame.Surface((hud_width * 2, sc_y_obj))
        self.right_hud.fill(grey)

        self.obstacles = [
            self.top_hud.get_rect(),
            self.left_hud.get_rect(),
            self.bottom_hud.get_rect(topleft=(0, sc_y_obj - hud_width)),
            self.right_hud.get_rect(topleft=(sc_x_obj - hud_width * 2, 0)),
        ]

        self.hero = Hero((sc_x_obj / 2, sc_y_obj / 2), 3)
        self.group = pygame.sprite.Group([self.hero])

    def setup(self):
        pass

    def update(self):
        self.hero.move(self.obstacles)

    def render(self):
        self.screen.fill(black)
        self.screen.blit(self.top_hud, (0, 0))
        self.screen.blit(self.left_hud, (0, 0))
        self.screen.blit(self.right_hud, (sc_x_obj - hud_width * 2, 0))
        self.screen.blit(self.bottom_hud, (0, sc_y_obj - hud_width))
        self.hero.draw(self.screen)
        # self.group.draw(self.screen)
        drTest()       

    def handle_event(self, event):
        pass

    def cleanup(self):
        pass


class SceneManager:
    def __init__(self, screen):
        self.screen = screen
        self.scenes = {}
        self.current_scene = None

    def add_scene(self, scene_name, scene):
        if isinstance(scene, SceneBase):
            self.scenes[scene_name] = scene

    def switch_scene(self, scene_name):
        if self.current_scene is not None:
            self.current_scene.cleanup()

        self.current_scene = self.scenes.get(scene_name)

        if self.current_scene is not None:
            self.current_scene.setup()
        else:
            print("Name is not found")

    def run_current_scene(self):
        if self.current_scene is not None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.current_scene.handle_event(event)

            self.current_scene.update()
            self.current_scene.render()
