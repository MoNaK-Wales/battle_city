import pygame
from Score import Scores

# ...existing code...

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Battle City")
    
    stats = GameStats()
    scores = Scores(screen, stats)
    
    # Змінна для відстеження стану паузи
    game_paused = False
    
    # Спрайт паузи
    pause_image = pygame.image.load('pause.png')
    pause_rect = pause_image.get_rect()
    pause_rect.center = screen.get_rect().center

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_paused = not game_paused
        
        if not game_paused:
            # Оновлення гри
            # ...existing game update logic...
            pass
        
        # Очищення екрану
        screen.fill((0, 0, 0))
        
        if game_paused:
            # Відображення спрайту паузи
            screen.blit(pause_image, pause_rect)
        else:
            # Відображення гри
            scores.show_score()
            # ...existing game draw logic...
        
        pygame.display.flip()

if __name__ == '__main__':
    run_game()