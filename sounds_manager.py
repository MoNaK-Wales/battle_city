import pygame


class SoundsManager:
    pygame.mixer.init()

    channel_player = pygame.mixer.Channel(1)  # Канал для игрока
    channel_enemy = pygame.mixer.Channel(2)
    start_music = pygame.mixer.Sound("assets\sounds\start music.mp3")
    hero_running_music = pygame.mixer.Sound("assets\sounds\\running.wav")
    hero_running_music.set_volume(0.4)
    enemy_running_music = pygame.mixer.Sound("assets\sounds\\running 2.wav")
    enemy_running_music.set_volume(0.4)
    bullet_init_music = pygame.mixer.Sound("assets\sounds\shooting.wav")
    bullet_wall_music = pygame.mixer.Sound("assets\sounds\shooting wall.wav")
    bullet_bricks_music = pygame.mixer.Sound("assets\sounds\shooting bricks.wav")
    enemy_destroyed_music = pygame.mixer.Sound("assets\sounds\enemy destroy.wav")

    @staticmethod
    def startlevel():
        SoundsManager.start_music.play()

    @staticmethod
    def hero_running(pos, initial_pos):
        if pos != initial_pos:
            if not SoundsManager.channel_player.get_busy():
                SoundsManager.channel_player.play(SoundsManager.hero_running_music, -1)
        else:
            SoundsManager.channel_player.stop()

    @staticmethod
    def enemy_running(pos, initial_pos):
        if pos != initial_pos:
            if not SoundsManager.channel_enemy.get_busy() and not SoundsManager.channel_player.get_busy():
                SoundsManager.channel_enemy.play(SoundsManager.enemy_running_music, -1)
        else:
            SoundsManager.channel_enemy.stop()

    @staticmethod
    def bullet_init():
        SoundsManager.channel_player.play(SoundsManager.bullet_init_music)

    @staticmethod
    def bullet_wall():
        SoundsManager.channel_player.play(SoundsManager.bullet_wall_music)

    @staticmethod    
    def bullet_bricks():
        SoundsManager.channel_player.play(SoundsManager.bullet_bricks_music)

    @staticmethod
    def enemy_destroyed():
        SoundsManager.channel_player.play(SoundsManager.enemy_destroyed_music)