import pygame
from setting import *
from entities.player import Player

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)

    clock = pygame.time.Clock()

    player = Player(100, 100, 50, 5)

    running = True
    while running:
        clock.tick(30) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        player.handle_input()
        screen.fill((0, 0, 0))
        player.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()