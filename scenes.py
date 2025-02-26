import pygame
import sys
import level_manager
import tanks
import time
from itertools import cycle
from os import path
from abc import ABC, abstractmethod
from constants import *
from set_sprites import AddableGroup, Base
from logger import logger
from strategies import NoMovement
from sounds_manager import SoundsManager
from score_manager import ScoreManager


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
        self.logo_rect.center = (SC_X_OBJ / 2, SC_Y_OBJ * 0.57)

        self.tank_logo = pygame.transform.scale_by(
            pygame.image.load("assets/misc/tank_logo.png").convert(), 0.14 * SC_SCALE
        )
        self.tank_logo_rect = self.tank_logo.get_rect()
        self.tank_logo_rect.center = (SC_X_OBJ / 2, SC_Y_OBJ * 0.23)

    def setup(self):
        logger.info("Menu setup")

        score, score_rect, score_plus, score_plus_rect = ScoreManager.render(WHITE)

        self.screen.fill(self.background_color)
        self.screen.blit(self.start_button, self.start_button_rect)
        self.screen.blit(self.logo, self.logo_rect)
        self.screen.blit(self.tank_logo, self.tank_logo_rect)
        self.screen.blit(score, score_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if self.start_button_rect.collidepoint(mouse_x, mouse_y):
                logger.debug(f"LMB click on start button at {event.pos}")
                new_stage = StageLoader(self.screen, self.scene_manager, 1)
                self.scene_manager.add_scene("StageLoader 1", new_stage)
                self.scene_manager.switch_scene("StageLoader 1")
        elif event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_RETURN]:  # enter
                logger.debug(f"Starting game via enter")
                new_stage = StageLoader(self.screen, self.scene_manager, 1)
                self.scene_manager.add_scene("StageLoader 1", new_stage)
                self.scene_manager.switch_scene("StageLoader 1")

    def render(self):
        pass

    def update(self):
        pass

    def cleanup(self):
        logger.info("Menu cleanup")

        ScoreManager.clear_score()


class Stage(SceneBase):
    def __init__(self, screen, scene_manager, level, hero_factory):
        super().__init__(screen, scene_manager)

        self.level = level
        self.map = "assets/stages/stage" + str(level)
        self.level_manager = level_manager.LevelLoader(self.map)
        self.hero_factory = hero_factory

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

        self.end_delay = GAMEOVER_TIME
        self.last_kill_timer = None

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

        level_obstacles, spawnpoint, base_pos, enemy_spawns, enemy_types = self.level_manager.load()

        self.base = Base(base_pos, self, self.animations_group)

        self.obstacles_group = AddableGroup(level_obstacles)
        self.obstacles_group.add(self.base)
        self.hero_group = AddableGroup()
        self.bullets = AddableGroup()
        self.enemies_group = AddableGroup()

        enemy_factories = [
            tanks.EnemyFactory(enemy_spawns[1], self.animations_group, enemy_types[1]),
            tanks.EnemyFactory(enemy_spawns[2], self.animations_group, enemy_types[2]),
            tanks.EnemyFactory(enemy_spawns[0], self.animations_group, enemy_types[0]),
        ]
        self.factories_iter = cycle(enemy_factories)
        self.enemy_spawn_count = DEBUG_ENEMIES_AMOUNT #20
        
        # фабрика героя будет передаваться между уровнями и хранить в ней героя (если его не будет, то создавать)
        # на первый уровень фабрики ещё не существует, а в следующих будут обновляться её атрибуты
        if self.hero_factory is None:
            self.hero_factory = tanks.HeroFactory(spawnpoint, self.animations_group, self.hero_group, self.game_over) 
        elif isinstance(self.hero_factory, tanks.HeroFactory):
            self.hero_factory.spawnpoint = spawnpoint
            self.hero_factory.hero.pos = spawnpoint
            self.hero_factory.anims_group = self.animations_group
            self.hero_factory.hero.expl_group = self.animations_group
            self.hero_factory.hero_group = self.hero_group
            self.hero_factory.gameover_func = self.game_over
        else:
            logger.error("Hero Factory's type is not correct")

        self.hero_factory.spawn()

        self.hp_number_font = pygame.font.Font(NES_FONT, SMALL_FONT_SIZE * SC_SCALE)
        self.hp_number = self.hp_number_font.render(f"{self.hero_factory.hero.hp}", False, BLACK, GREY)
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
        self.enemies_group.update(**kwargs)
        self.bullets.update(**kwargs)
        self.animations_group.update()
        self.hero_group.update(**hero_kwargs)

        self.enemies_count_rects = self.enemies_count_rects[: self.enemy_spawn_count]

        self.hp_number = self.hp_number_font.render(f"{self.hero_factory.hero.hp}", False, BLACK, GREY)

        if ScoreManager.score // HP_UP_SCORE > ScoreManager.given_hp_up:
            self.hero_factory.hero.hp += 1
            ScoreManager.given_hp_up += 1
            SoundsManager.hp_up()

        if self.gameover and self.gameover_rect.centery > SC_Y_OBJ / 2:
            self.gameover_rect.centery -= 1 * SC_SCALE

        if self.gameover:
            if self.gameover_timer > self.end_delay:
                next_scene = ScoreScene(self.screen, self.scene_manager)
                self.scene_manager.add_scene("Game over score", next_scene)
                self.scene_manager.switch_scene("Game over score")
            else:
                self.gameover_timer += 1

        self.check_level_end()

    def render(self):
        score, score_rect, score_plus, score_plus_rect = ScoreManager.render(BLACK)
        self.screen.fill(self.background_color)
        self.screen.blit(self.top_hud, (0, 0))
        self.screen.blit(self.left_hud, (0, 0))
        self.screen.blit(self.right_hud, (SC_X_OBJ - HUD_WIDTH * 2, 0))
        self.screen.blit(self.bottom_hud, (0, SC_Y_OBJ - HUD_WIDTH))
        self.hero_group.draw(self.screen)
        self.enemies_group.draw(self.screen)
        self.obstacles_group.draw(self.screen)
        self.bullets.draw(self.screen)
        self.animations_group.draw(self.screen)
        self.screen.blit(self.hp_label, self.hp_label_rect)
        self.screen.blit(self.hp_icon, self.hp_icon_rect)
        self.screen.blit(self.hp_number, self.hp_number_rect)
        self.screen.blit(self.stage_number_icon, self.stage_number_icon_rect)
        self.screen.blit(self.stage_number, self.stage_number_rect)
        self.screen.blit(self.gameover_image, self.gameover_rect)
        self.screen.blit(score, score_rect)
        self.screen.blit(score_plus, score_plus_rect)

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
                if not self.gameover:
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
            if self.last_kill_timer is None:
                self.last_kill_timer = 0
                ScoreManager.add("Level")

            if self.last_kill_timer > self.end_delay:
                if path.isfile("assets/stages/stage" + str(self.level + 1)):
                    logger.info(f"Loading {self.level + 1} stage")
                    next_scene = ScoreScene(self.screen, self.scene_manager, False, self.level + 1, self.hero_factory)
                    self.scene_manager.add_scene(f"ScoreScene {self.level + 1}", next_scene)
                    self.scene_manager.switch_scene(f"ScoreScene {self.level + 1}")
                else:
                    logger.warning(f"New Stage is not found, starting from 1")
                    next_scene = ScoreScene(self.screen, self.scene_manager, False, 1, self.hero_factory)
                    self.scene_manager.add_scene(f"ScoreScene 1", next_scene)
                    self.scene_manager.switch_scene(f"ScoreScene 1")
            else:
                self.last_kill_timer += 1

    def game_over(self):
        logger.info("Game Over")
        self.hero_factory.hero.strategy = NoMovement()
        self.gameover = True


class StageLoader(SceneBase):
    def __init__(self, screen, scene_manager, level, hero_factory = None):
        super().__init__(screen, scene_manager)

        self.background_color = GREY
        self.level = level
        self.hero_factory = hero_factory

        self.stage_font = pygame.font.Font(NES_FONT, FONT_SIZE * SC_SCALE)
        self.stage_text = self.stage_font.render(
            f"STAGE {self.level}", False, BLACK, GREY
        )
        self.stage_text_rect = self.stage_text.get_rect()
        self.stage_text_rect.center = (SC_X_OBJ / 2, SC_Y_OBJ / 2)

        self.next_scene = Stage(self.screen, self.scene_manager, self.level, self.hero_factory)

        self.screen_time = FPS * STAGELOADER_TIME
        self.timer = 0

    def setup(self):
        logger.info("StageLoader setup")

        SoundsManager.pause(True)
        SoundsManager.pause(False)
        SoundsManager.startlevel()

    def update(self):
        if self.timer >= self.screen_time:
            self.scene_manager.add_scene(f"Stage {self.level}", self.next_scene)
            self.scene_manager.switch_scene(f"Stage {self.level}")
        else:
            self.timer += 1

    def render(self):
        self.screen.fill(self.background_color)
        self.screen.blit(self.stage_text, self.stage_text_rect)

    def handle_event(self, event):
        pass

    def cleanup(self):
        logger.info("StageLoader cleanup")


class GameOver(SceneBase):
    def __init__(self, screen, scene_manager):
        super().__init__(screen, scene_manager)

        self.gameover_icon = pygame.transform.scale_by(pygame.image.load("assets/misc/gameover_screen.png").convert_alpha(), SC_SCALE)
        self.gameover_icon_rect = self.gameover_icon.get_rect()
        self.gameover_icon_rect.center = (SC_X_OBJ / 2, SC_Y_OBJ / 2)

        self.screen_time = FPS * GAMEOVER_SCREEN_TIME
        self.timer = 0

    def setup(self):
        logger.info("GAME OVER screen")

        SoundsManager.pause(True)
        SoundsManager.pause(False)
        SoundsManager.gameover()
    
    def update(self):
        if self.timer >= self.screen_time:
            self.scene_manager.switch_scene("Menu")
        else:
            self.timer += 1
    
    def render(self):
        self.screen.blit(self.gameover_icon, self.gameover_icon_rect)
    
    def handle_event(self, event):
        pass
    
    def cleanup(self):
        pass


class ScoreScene(SceneBase):
    def __init__(self, screen, scene_manager, is_gameover = True, level = None, hero_factory = None):
        super().__init__(screen, scene_manager)

        self.background_color = BLACK
        self.level = level
        self.hero_factory = hero_factory

        self.stage_score = ScoreManager.stage_adding
        self.total_score_was = ScoreManager.score - ScoreManager.stage_adding

        self.stage_added_score = 0
        self.total_added_score = self.total_score_was

        self.scoring_frame_delay = 1/7 * FPS
        self.next_scene_delay = STAGELOADER_TIME * FPS
        self.stage_scoring_timer = 0
        self.total_scoring_timer = -1
        self.next_scene_timer = -1
        
        """
        STAGE PTS: 00000
        TOTAL PTS: 00000
        """

        self.stage_pts_str = "STAGE PTS: 00000"
        self.stage_pts_font = pygame.font.Font(NES_FONT, SMALL_FONT_SIZE * SC_SCALE)
        self.stage_pts_text = self.stage_pts_font.render(self.stage_pts_str, False, WHITE, BLACK)
        self.stage_pts_rect = self.stage_pts_text.get_rect()
        self.stage_pts_rect.midbottom = (SC_X_OBJ / 2, SC_Y_OBJ / 2)

        self.total_pts_str = f"TOTAL PTS: {self.total_score_was:05d}"
        self.total_pts_font = pygame.font.Font(NES_FONT, SMALL_FONT_SIZE * SC_SCALE)
        self.total_pts_text = self.total_pts_font.render(self.total_pts_str, False, WHITE, BLACK)
        self.total_pts_rect = self.total_pts_text.get_rect()
        self.total_pts_rect.midtop = (SC_X_OBJ / 2, SC_Y_OBJ / 2)

        if is_gameover:
            self.next_scene = "Game over"
        else:
            scene = StageLoader(self.screen, self.scene_manager, self.level, self.hero_factory)
            self.next_scene = f"StageLoader {self.level}"
            self.scene_manager.add_scene(self.next_scene, scene)

    def setup(self):
        logger.info("Score scene setup, saving high score")

        ScoreManager.save_high_score()

    def update(self):
        if self.stage_scoring_timer > self.scoring_frame_delay and self.total_scoring_timer == -1:
            if self.stage_added_score < self.stage_score:
                self.stage_added_score += 100
                self.stage_pts_str = f"STAGE PTS: {self.stage_added_score:05d}"
                SoundsManager.scoring()
                self.stage_scoring_timer = 0
            else:
                self.total_scoring_timer = -50.5  # чтобы была задержка и при этом он не был в значении -1
        else:
            self.stage_scoring_timer += 1

        if self.total_scoring_timer > self.scoring_frame_delay and self.next_scene_timer == -1:
            if self.total_added_score < ScoreManager.score:
                self.total_added_score += 100
                self.total_pts_str = f"TOTAL PTS: {self.total_added_score:05d}"
                SoundsManager.scoring()
                self.total_scoring_timer = 0
            else:
                self.next_scene_timer = 0
        elif self.total_scoring_timer != -1:
            self.total_scoring_timer += 1

        if self.next_scene_timer > self.next_scene_delay:
            self.scene_manager.switch_scene(self.next_scene)
        elif self.next_scene_timer != -1:
            self.next_scene_timer += 1

        
        self.stage_pts_text = self.stage_pts_font.render(self.stage_pts_str, False, WHITE, BLACK)
        self.total_pts_text = self.total_pts_font.render(self.total_pts_str, False, WHITE, BLACK)

    def render(self):
        score, score_rect, score_plus, score_plus_rect = ScoreManager.render(WHITE)

        self.screen.fill(self.background_color)
        self.screen.blit(score, score_rect)
        self.screen.blit(self.stage_pts_text, self.stage_pts_rect)
        self.screen.blit(self.total_pts_text, self.total_pts_rect)

    def handle_event(self, event):
        pass

    def cleanup(self):
        ScoreManager.stage_adding = 0


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
