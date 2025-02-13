import pygame
import sys


NES_font = "assets/fonts/nes-font.ttf"


class SceneBase:
    pass

class Menu(SceneBase):
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager

        self.menu_font = pygame.font.Font("assets/fonts/nes-font.ttf", 36)
        self.start_button = self.menu_font.render('START GAME', False, (255, 255, 255), (0, 0, 0))
        self.start_button_rect = self.start_button.get_rect()
        self.start_button_rect.center = (400, 700)

        self.logo = pygame.transform.scale_by(pygame.image.load("assets/misc/logo.png").convert(), 2)
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.center = (400, 550)
        
        self.tank_logo = pygame.transform.scale_by(pygame.image.load("assets/misc/tank_logo.png").convert(), 0.75)
        self.tank_logo_rect = self.tank_logo.get_rect()
        self.tank_logo_rect.center = (400, 250)
         

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