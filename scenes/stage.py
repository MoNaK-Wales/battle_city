import pygame
import managers.level_manager as level_manager
import sprites.tanks as tanks
import time
from itertools import cycle
from os import path
from constants import *
from scenes.base_scenes import SceneBase
import scenes.stage_loader
from sprites.set_sprites import AddableGroup
from sprites.obstacles import Base
from managers.logger import logger
from strategies.base_strategy import NoMovement
from managers.sounds_manager import SoundsManager


class Stage(SceneBase):

    def __init__(self, screen, scene_manager, level):
        super().__init__(screen, scene_manager)

        self.level = level
        self.map = "assets/stages/stage" + str(level)
        self.level_manager = level_manager.LevelLoader(self.map)

        self.background_color = BLACK

        self.top_hud = pygame.Surface((SC_X_OBJ, HUD_WIDTH))
        self.top_hud.fill(GREY)
        self.left_hud = pygame.Surface((HUD_WIDTH, SC_Y_OBJ))
        self.left_hud.fill(GREY)
        self.bottom_hud = pygame.Surface((SC_X_OBJ, HUD_WIDTH))
        self.bottom_hud.fill(GREY)
        self.right_hud = pygame.Surface((HUD_WIDTH * 2, SC_Y_OBJ))
        self.right_hud.fill(GREY)

        self.hud = [
            self.top_hud.get_rect(),
            self.left_hud.get_rect(),
            self.bottom_hud.get_rect(topleft=(0, SC_Y_OBJ - HUD_WIDTH)),
            self.right_hud.get_rect(topleft=(SC_X_OBJ - HUD_WIDTH * 2, 0)),
        ]

        self.lastspawn = 0
        self.gameover_timer = 0

        self.gameover = False
        self.gameover_image = pygame.transform.scale_by(
            pygame.image.load("assets/misc/game_over.png").convert_alpha(), SC_SCALE
        )
        self.gameover_rect = self.gameover_image.get_rect(
            center=(SC_X_OBJ / 2 - HUD_WIDTH, SC_Y_OBJ + 50)
        )

        self.enemies_count_rects = []
        for height in range(10):
            for width in range(2):
                self.enemies_count_rects.append(
                    pygame.Rect(
                        SC_X_OBJ - 24 * SC_SCALE + TILE_SIZE * width,
                        24 * SC_SCALE + TILE_SIZE * height,
                        TILE_SIZE,
                        TILE_SIZE,
                    )
                )
        self.enemies_count_image = pygame.transform.scale_by(
            pygame.image.load("assets/misc/HUD/enemies.png"), SC_SCALE
        )

        self.hp_font = pygame.font.Font(NES_FONT, SMALL_FONT_SIZE * SC_SCALE)
        self.hp_label = self.hp_font.render("HP", False, BLACK, GREY)
        self.hp_label_rect = self.hp_label.get_rect(center=(SC_X_OBJ - 16 * SC_SCALE, 140 * SC_SCALE))
        self.hp_icon = pygame.transform.scale_by(pygame.image.load("assets/misc/HUD/lifes.png"), SC_SCALE)
        self.hp_icon_rect = self.hp_icon.get_rect(center=(SC_X_OBJ - 21 * SC_SCALE, 148 * SC_SCALE))

        self.stage_font = pygame.font.Font(NES_FONT, SMALL_FONT_SIZE * SC_SCALE)
        self.stage_number = self.stage_font.render("{:02}".format(self.level), False, BLACK, GREY)
        self.stage_number_rect = self.stage_number.get_rect(center=(SC_X_OBJ - 16 * SC_SCALE, SC_Y_OBJ - 36 * SC_SCALE))
        self.stage_number_icon = pygame.transform.scale_by(pygame.image.load("assets/misc/HUD/stage_number.png"), SC_SCALE)
        self.stage_number_icon_rect = self.stage_number_icon.get_rect(center=(SC_X_OBJ - 16 * SC_SCALE, SC_Y_OBJ - 48 * SC_SCALE))
        
        self.animations_group = AddableGroup()

        self.end_delay = 5
        self.last_kill_time = None

        self.pause = False
        self.pause_image = pygame.transform.scale_by(
            pygame.image.load("assets/misc/pause.png").convert_alpha(), SC_SCALE
        )
        self.pause_rect = self.pause_image.get_rect(
            center=((SC_X_OBJ - HUD_WIDTH) / 2, SC_Y_OBJ / 2 + 7 * SC_SCALE)
        )
        self.pause_blink_delay = 0.5
        self.pause_show = True
        self.last_pause_show = 0

    def setup(self):
        logger.info("Stage setup")

        level_obstacles, spawnpoint, base_pos, enemy_spawns = self.level_manager.load()

        self.hero = tanks.Hero(spawnpoint, 3, self.animations_group)
        self.base = Base(base_pos, self, self.animations_group)

        self.obstacles_group = AddableGroup(level_obstacles)
        self.obstacles_group.add(self.base)
        self.hero_group = AddableGroup(self.hero)
        self.bullets = AddableGroup()
        self.enemies_group = AddableGroup()

        enemy_types = [
            [0, 0, 0, 0, 0, 0],                     #временно для проверки
            [0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0]
        ]
        enemy_factories = [
            tanks.EnemyFactory(enemy_spawns[1], enemy_types[1], self.animations_group),
            tanks.EnemyFactory(enemy_spawns[2], enemy_types[2], self.animations_group),
            tanks.EnemyFactory(enemy_spawns[0], enemy_types[0], self.animations_group),
        ]
        self.factories_iter = cycle(enemy_factories)
        self.enemy_spawn_count = 20

        self.hp_number_font = pygame.font.Font(NES_FONT, SMALL_FONT_SIZE * SC_SCALE)
        self.hp_number = self.hp_number_font.render(f"{self.hero.hp}", False, BLACK, GREY)
        self.hp_number_rect = self.stage_number_icon.get_rect(size=(TILE_SIZE, TILE_SIZE))
        self.hp_number_rect.center = (SC_X_OBJ - 11 * SC_SCALE, 148 * SC_SCALE)

        logger.debug(f"Starting obstacles (HUD): {self.hud}")

    def update(self):
        if self.pause:
            return
        
        kwargs = {
            "obstacles": self.obstacles_group,
            "entities": self.hero_group + self.enemies_group,
            "hud": self.hud,
            "bullets": self.bullets,
            "anims": self.animations_group,
        }
        hero_kwargs = kwargs.copy()
        hero_kwargs.update(entities=self.enemies_group)

        self.spawn_enemy()
        self.hero_group.update(**hero_kwargs)
        self.enemies_group.update(**kwargs)
        self.bullets.update(**kwargs)
        self.animations_group.update()

        self.enemies_count_rects = self.enemies_count_rects[: self.enemy_spawn_count]

        self.hp_number = self.hp_number_font.render(f"{self.hero.hp}", False, BLACK, GREY)

        if self.gameover and self.gameover_rect.centery > SC_Y_OBJ / 2:
            self.gameover_rect.centery -= 1 * SC_SCALE

        if self.gameover and time.time() - self.gameover_timer > 10:
            self.scene_manager.switch_scene("Menu")

        self.check_level_end()

    def render(self):
        self.screen.fill(self.background_color)
        self.screen.blit(self.top_hud, (0, 0))
        self.screen.blit(self.left_hud, (0, 0))
        self.screen.blit(self.right_hud, (SC_X_OBJ - HUD_WIDTH * 2, 0))
        self.screen.blit(self.bottom_hud, (0, SC_Y_OBJ - HUD_WIDTH))
        self.bullets.draw(self.screen)
        self.hero_group.draw(self.screen)
        self.enemies_group.draw(self.screen)
        self.obstacles_group.draw(self.screen)
        self.animations_group.draw(self.screen)
        self.screen.blit(self.hp_label, self.hp_label_rect)
        self.screen.blit(self.hp_icon, self.hp_icon_rect)
        self.screen.blit(self.hp_number, self.hp_number_rect)
        self.screen.blit(self.stage_number_icon, self.stage_number_icon_rect)
        self.screen.blit(self.stage_number, self.stage_number_rect)
        self.screen.blit(self.gameover_image, self.gameover_rect)

        for rect in self.enemies_count_rects:
            self.screen.blit(self.enemies_count_image, rect)

        if self.pause:
            if self.pause_show:
                    self.screen.blit(self.pause_image, self.pause_rect)
            if time.time() - self.last_pause_show > self.pause_blink_delay:
                self.last_pause_show = time.time()
                self.pause_show = not self.pause_show

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_RETURN] or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                logger.info("Pause")
                self.pause = not self.pause
                SoundsManager.pause(self.pause)
                SoundsManager.pause_play()

    def cleanup(self):
        logger.info("Stage cleanup")

    def spawn_enemy(self):
        time_between_spawning = time.time() - self.lastspawn
        if (
            len(self.enemies_group) < 4
            and time_between_spawning > 3
            and self.enemy_spawn_count > 0
        ):
            factory = next(self.factories_iter)
            factory.spawn(self.enemies_group)
            self.enemy_spawn_count -= 1
            logger.info(f"Enemies not spawned yet count: {self.enemy_spawn_count}")
            self.lastspawn = time.time()

    def check_level_end(self):
        if self.enemy_spawn_count == 0 and len(self.enemies_group) == 0:
            if self.last_kill_time is None:
                self.last_kill_time = time.time()

            if time.time() - self.last_kill_time > self.end_delay:
                if path.isfile("assets/stages/stage" + str(self.level + 1)):
                    logger.info(f"Loading {self.level + 1} stage")
                    next_scene = scenes.stage_loader.StageLoader(self.screen, self.scene_manager, self.level + 1)
                    self.scene_manager.add_scene(f"StageLoader {self.level + 1}", next_scene)
                    self.scene_manager.switch_scene(f"StageLoader {self.level + 1}")
                else:
                    logger.warning(f"New Stage is not found, starting from 1")
                    next_scene = scenes.stage_loader.StageLoader(self.screen, self.scene_manager, 1)
                    self.scene_manager.add_scene(f"StageLoader 1", next_scene)
                    self.scene_manager.switch_scene(f"StageLoader 1")

    def game_over(self):
        logger.info("Game Over")
        self.hero.strategy = NoMovement()
        self.gameover_timer = time.time()
        self.gameover = True