import pygame
import sys
import level_manager
import tanks
import time
from itertools import cycle
from abc import ABC, abstractmethod
from constants import *
from logger import logger


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
                self.scene_manager.switch_scene("Stage 1")
        elif event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_RETURN]:  # enter
                logger.debug(f"Starting game via enter")
                self.scene_manager.switch_scene("Stage 1")

    def render(self):
        pass

    def update(self):
        pass

    def cleanup(self):
        logger.info("Menu cleanup")


class Stage(SceneBase):
    def __init__(self, screen, scene_manager, map):
        self.screen = screen
        self.scene_manager = scene_manager
        self.map = map
        self.level_manager = level_manager.LevelLoader(map)

        self.background_color = BLACK

        self.top_hud = pygame.Surface((SC_X_OBJ, HUD_WIDTH))
        self.top_hud.fill(GREY)
        self.left_hud = pygame.Surface((HUD_WIDTH, SC_Y_OBJ))
        self.left_hud.fill(GREY)
        self.bottom_hud = pygame.Surface((SC_X_OBJ, HUD_WIDTH))
        self.bottom_hud.fill(GREY)
        self.right_hud = pygame.Surface((HUD_WIDTH * 2, SC_Y_OBJ))
        self.right_hud.fill(GREY)

        self.obstacles = [
            self.top_hud.get_rect(),
            self.left_hud.get_rect(),
            self.bottom_hud.get_rect(topleft=(0, SC_Y_OBJ - HUD_WIDTH)),
            self.right_hud.get_rect(topleft=(SC_X_OBJ - HUD_WIDTH * 2, 0)),
        ]

        self.lastspawn = 0

    def setup(self):
        logger.info("Stage setup")

        level_obstacles, spawnpoint, enemy_spawns = self.level_manager.load()
        self.obstacles += level_obstacles

        self.hero = tanks.Hero(spawnpoint, 3)
        self.group = pygame.sprite.Group()
        self.group.add(self.hero)
        self.group.add(level_obstacles)
        self.bullets = pygame.sprite.Group()

        self.enemies_group = pygame.sprite.Group()

        enemy_types = [
            [0, 0, 0, 0, 0, 0],                     #временно для проверки
            [0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0]
        ]
        enemy_factories = [
            tanks.EnemyFactory(enemy_spawns[1], enemy_types[1]),
            tanks.EnemyFactory(enemy_spawns[2], enemy_types[2]),
            tanks.EnemyFactory(enemy_spawns[0], enemy_types[0]),
        ]
        self.factories_iter = cycle(enemy_factories)
        self.enemy_count = 0

        logger.debug(f"Starting obstacles (HUD): {self.obstacles}")

    def update(self):
        self.hero.move(self.obstacles, None, self.enemies_group, self.bullets)
        self.spawn_enemy()
        self.group.update()
        self.enemies_group.update()
        self.bullets.update(obstacles=self.obstacles, entitys=self.hero, enemy=self.enemies_group)

    def render(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.top_hud, (0, 0))
        self.screen.blit(self.left_hud, (0, 0))
        self.screen.blit(self.right_hud, (SC_X_OBJ - HUD_WIDTH * 2, 0))
        self.screen.blit(self.bottom_hud, (0, SC_Y_OBJ - HUD_WIDTH))
        self.bullets.draw(self.screen)
        self.group.draw(self.screen)
        self.enemies_group.draw(self.screen)

    def handle_event(self, event):
        pass

    def cleanup(self):
        logger.info("Stage cleanup")

    def spawn_enemy(self):
        timenow = time.time() - self.lastspawn
        if len(self.enemies_group) < 4 and timenow > 5:
            factory = next(self.factories_iter)
            new_enemy = factory.spawn()
            self.enemies_group.add(new_enemy)
            self.lastspawn = time.time()


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
