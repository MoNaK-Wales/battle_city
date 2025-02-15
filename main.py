import pygame
import sys
from scenes import *
from constants import *




# def show_menu(screen):
#     # menu_font = pygame.font.SysFont(None, 48)
#     # start_button = menu_font.render('Почати', True, (255, 255, 255), (0, 0, 0))
#     # start_button_rect = start_button.get_rect()
#     # start_button_rect.center = screen.get_rect().center

#     menu_font = pygame.font.Font("assets/fonts/nes-font.ttf", 32)
#     start_button = menu_font.render('START GAME', False, (255, 255, 255), (0, 0, 0))
#     start_button_rect = start_button.get_rect()
#     start_button_rect.center = (400, 700)

#     logo = pygame.image.load("assets/misc/logo.png").convert()
#     logo_rect = logo.get_rect()
#     logo_rect.center = (400, 550)
    
#     tank_logo = pygame.transform.scale_by(pygame.image.load("assets/misc/tank_logo.png").convert(), 0.75)
#     tank_logo_rect = tank_logo.get_rect()
#     tank_logo_rect.center = (400, 225)

#     # Завантаження вашої картинки
#     # background_image = pygame.image.load('images.png')
#     # background_rect = background_image.get_rect()
#     # background_rect.center = screen.get_rect().center

#     while True:
#         screen.fill((0, 0, 0))
#         # screen.blit(background_image, background_rect)
#         screen.blit(start_button, start_button_rect)
#         screen.blit(logo, logo_rect)
#         screen.blit(tank_logo, tank_logo_rect)
#         pygame.display.flip()

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 mouse_x, mouse_y = event.pos
#                 if start_button_rect.collidepoint(mouse_x, mouse_y):
#                     return  # Вихід з меню і початок гри

def run_game():
    pygame.init()
    screen = pygame.display.set_mode(sc_size)  #ВЫБРАТЬ РАЗРЕШЕНИЕ
    pygame.display.set_caption("Battle City")

    scene_manager = SceneManager(screen)
    menu = Menu(screen, scene_manager)
    stage1 = Stage(screen, scene_manager, "assets/stages/")
    scene_manager.add_scene("Menu", menu)
    scene_manager.add_scene("Stage 1", stage1)
    scene_manager.switch_scene("Menu")
    
    # Показати меню перед початком гри
    # show_menu(screen)

    while True:
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         sys.exit()
        
        # Оновлення гри
        # ...existing game update logic...
        
        # Очищення екрану
        # screen.fill((0, 0, 0))
        
        # Відображення гри
        # ...existing game draw logic...
        
        scene_manager.run_current_scene()

        pygame.display.flip()

if __name__ == '__main__':
    run_game()