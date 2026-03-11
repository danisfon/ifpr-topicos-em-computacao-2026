import pygame
from entities.player import Player, resolve_collision


def draw_exit_button(screen, font):
    button_text = font.render("[ ESC ] Sair", True, (255, 255, 255))

    btn_rect = button_text.get_rect(
        bottomright=(screen.get_width() - 10, screen.get_height() - 10)
    )

    bg_surf = pygame.Surface((btn_rect.width + 10, btn_rect.height + 6), pygame.SRCALPHA)
    bg_surf.fill((0, 0, 0, 150))

    screen.blit(bg_surf, (btn_rect.x - 5, btn_rect.y - 3))
    screen.blit(button_text, btn_rect)


def run_game(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 20)

    track_image = pygame.image.load("assets/track.png").convert()
    track_image = pygame.transform.scale(
        track_image, (screen.get_width(), screen.get_height())
    )

    controls_player1 = {
        "left": pygame.K_a,
        "right": pygame.K_d,
        "up": pygame.K_w,
        "down": pygame.K_s,
    }

    controls_player2 = {
        "left": pygame.K_LEFT,
        "right": pygame.K_RIGHT,
        "up": pygame.K_UP,
        "down": pygame.K_DOWN,
    }

    player1 = Player(
        300, 500, 40, controls_player1, (160, 32, 230),
        screen.get_width(), screen.get_height()
    )

    player2 = Player(
        900, 500, 40, controls_player2, (255, 0, 0),
        screen.get_width(), screen.get_height()
    )

    running = True

    while running:
        delta_time = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"

        player1.handle_input(delta_time)
        player2.handle_input(delta_time)

        resolve_collision(player1, player2)

        screen.blit(track_image, (0, 0))
        player1.draw(screen)
        player2.draw(screen)

        draw_exit_button(screen, font)

        pygame.display.flip()

    return "menu"