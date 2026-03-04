import pygame
from setting import *
from entities.player import Player, resolve_collision


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)

    clock = pygame.time.Clock()

    controls_player1 = {
        "left":  pygame.K_a,
        "right": pygame.K_d,
        "up":    pygame.K_w,
        "down":  pygame.K_s,
    }

    controls_player2 = {
        "left":  pygame.K_LEFT,
        "right": pygame.K_RIGHT,
        "up":    pygame.K_UP,
        "down":  pygame.K_DOWN,
    }

    player1 = Player(100, 100, 50, controls_player1, (160, 32, 230))
    player2 = Player(300, 300, 50, controls_player2, (255, 0, 0))

    running = True
    while running:
        # delta_time in seconds — used in: position += velocity * delta_time
        delta_time = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update movement
        player1.handle_input(delta_time)
        player2.handle_input(delta_time)

        # Resolve collision between the two players
        resolve_collision(player1, player2)

        screen.fill((0, 0, 0))
        player1.draw(screen)
        player2.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()