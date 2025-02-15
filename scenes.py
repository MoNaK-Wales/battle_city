import pygame
import sys
import constants
from abc import ABC, abstractmethod



class SceneBase(ABC):
    @abstractmethod
    def render(self):
        pass
    
    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def handle_event(self, event):
        pass

    @abstractmethod
    def setup(self):
        pass
    
    @abstractmethod
    def cleanup(self):
        pass

class Menu(SceneBase):
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager

        self.background_color = constants.black

        self.menu_font = pygame.font.Font(constants.NES_font, 32)
        self.start_button = self.menu_font.render('START GAME', False, constants.white, constants.black)
        self.start_button_rect = self.start_button.get_rect()
        self.start_button_rect.center = (400, 700)

        self.logo = pygame.image.load("assets/misc/logo.png").convert()
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.center = (400, 550)
        
        self.tank_logo = pygame.transform.scale_by(pygame.image.load("assets/misc/tank_logo.png").convert(), 0.75)
        self.tank_logo_rect = self.tank_logo.get_rect()
        self.tank_logo_rect.center = (400, 225)

    def render(self):
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
            if event.key == pygame.K_KP_ENTER:
                self.scene_manager.switch_scene("Stage 1")

    def update(self):
        pass

    def setup(self):
        pass

    def cleanup(self):
        pass

class Stage(SceneBase):
    def __init__(self, screen, scene_manager, map):
        self.screen = screen
        self.scene_manager = scene_manager
        self.map = map

        self.background_color = constants.black

        self.top_hud = pygame.Surface((800, 48))
        self.top_hud.fill(constants.grey)
        self.left_hud = pygame.Surface((48, 800))
        self.left_hud.fill(constants.grey)
        self.bottom_hud = pygame.Surface((800, 48))
        self.bottom_hud.fill(constants.grey)
        self.right_hud = pygame.Surface((96, 800))
        self.right_hud.fill(constants.grey)

    def render(self):
        self.screen.fill(constants.black)
        self.screen.blit(self.top_hud, (0, 0))
        self.screen.blit(self.left_hud, (0, 0))
        self.screen.blit(self.right_hud, (704, 0))
        self.screen.blit(self.top_hud, (0, 752))

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def setup(self):
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

    def run_current_scene(self):
        if self.current_scene:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.current_scene.handle_event(event)

            self.current_scene.update()
            self.current_scene.render()