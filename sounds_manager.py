import pygame


class SoundsManager:
    pygame.mixer.init()

    start_music = pygame.mixer.Sound("assets/sounds/start music.mp3")
    gameover_music = pygame.mixer.Sound("assets/sounds/game over music.mp3")
    hero_running_music = pygame.mixer.Sound("assets/sounds/running.wav")
    hero_running_music.set_volume(0.4)
    enemy_running_music = pygame.mixer.Sound("assets/sounds/running 2.wav")
    enemy_running_music.set_volume(0.4)
    bullet_init_music = pygame.mixer.Sound("assets/sounds/shooting.wav")
    bullet_wall_music = pygame.mixer.Sound("assets/sounds/shooting wall.wav")
    bullet_bricks_music = pygame.mixer.Sound("assets/sounds/shooting bricks.wav")
    enemy_destroyed_music = pygame.mixer.Sound("assets/sounds/enemy destroy.wav")
    player_destroyed_music = pygame.mixer.Sound("assets/sounds/player destroy.wav")

    pause_music = pygame.mixer.Sound("assets/sounds/pause.wav")
    channel_pause = pygame.mixer.Channel(3)

    channel_player = pygame.mixer.Channel(1)  # Канал для игрока
    channel_player.play(hero_running_music, -1)
    channel_player.pause()
    channel_player_paused = True

    channel_enemy = pygame.mixer.Channel(2)  # Канал для врагов
    channel_enemy.play(enemy_running_music, -1)
    channel_enemy.pause()
    channel_enemy_paused = True

    @staticmethod
    def startlevel():
        SoundsManager.start_music.play()

    @staticmethod
    def gameover():
        SoundsManager.gameover_music.play()

    @staticmethod
    def hero_running(pos, initial_pos):
        if pos != initial_pos:
            SoundsManager.channel_player.unpause()
            SoundsManager.channel_player_paused = False
        else:
            SoundsManager.channel_player.pause()
            SoundsManager.channel_player_paused = True

    @staticmethod
    def enemy_running(is_on):
        if is_on and SoundsManager.channel_player_paused:
            SoundsManager.channel_enemy.unpause()
            channel_enemy_paused = False
        else:
            SoundsManager.channel_enemy.pause()
            channel_enemy_paused = True

    @staticmethod
    def bullet_init():
        SoundsManager.bullet_init_music.play()

    @staticmethod
    def bullet_wall():
        SoundsManager.bullet_wall_music.play()

    @staticmethod    
    def bullet_bricks():
        SoundsManager.bullet_bricks_music.play()

    @staticmethod
    def enemy_destroyed():
        SoundsManager.enemy_destroyed_music.play()

    @staticmethod
    def player_destroyed():
        SoundsManager.player_destroyed_music.play()

    @staticmethod
    def pause_play():
        SoundsManager.channel_pause.play(SoundsManager.pause_music)

    @staticmethod
    def pause(is_paused):
        if is_paused:
            pygame.mixer.pause()
        else:
            pygame.mixer.unpause()
            SoundsManager.channel_enemy.pause()
            SoundsManager.channel_enemy_paused = True
            SoundsManager.channel_player.pause()
            SoundsManager.channel_player_paused = True
