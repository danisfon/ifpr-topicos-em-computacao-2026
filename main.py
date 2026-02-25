import pygame
from setting import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            screen.fill((100,0,0))
            pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()