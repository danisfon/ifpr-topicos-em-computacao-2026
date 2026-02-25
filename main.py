import pygame
from setting import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)

    clock = pygame.time.Clock()

    x = 100
    y = 100
    size = 50
    speed = 5

    running = True
    while running:
        clock.tick(30) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            x -= speed
        if keys[pygame.K_RIGHT]:
            x += speed
        if keys[pygame.K_UP]:
            y -= speed
        if keys[pygame.K_DOWN]:
            y += speed

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 255, 0), (x, y, size, size))
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()