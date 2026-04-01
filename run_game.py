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


# 🔥 FUNÇÃO: detectar grama
def is_on_grass(player, track_image):
    x = int(player.position.x + player.size // 2)
    y = int(player.position.y + player.size // 2)

    # evita erro fora da tela
    if x < 0 or y < 0 or x >= track_image.get_width() or y >= track_image.get_height():
        return False

    color = track_image.get_at((x, y))
    r, g, b = color[:3]

    # detecta verde (grama)
    return g > r and g > b

def is_on_barrier(player, track_image):
    x = int(player.position.x + player.size // 2)
    y = int(player.position.y + player.size // 2)

    if x < 0 or y < 0 or x >= track_image.get_width() or y >= track_image.get_height():
        return False

    r, g, b, *_ = track_image.get_at((x, y))

    # 🔴 vermelho da zebra
    is_red = r > 200 and g < 80 and b < 80

    # ⚪ branco da zebra
    is_white = r > 200 and g > 200 and b > 200

    # 🚫 ignorar cinza (asfalto)
    is_gray = abs(r - g) < 20 and abs(r - b) < 20 and r < 180

    return (is_red or is_white) and not is_gray


def run_game(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 20)

    track_image = pygame.image.load("assets/nivel1.png").convert()
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

        # 🎮 movimentação
        player1.handle_input(delta_time)
        player2.handle_input(delta_time)

        # 🔥 GRAMA desacelera
        if is_on_grass(player1, track_image):
            player1.velocity.x *= 0.90
            player1.velocity.y *= 0.90

        if is_on_grass(player2, track_image):
            player2.velocity.x *= 0.90
            player2.velocity.y *= 0.90

        # 🚧 COLISÃO COM BARREIRA (AQUI 👇)
        if is_on_barrier(player1, track_image):
            player1.position -= player1.velocity   # volta
            player1.velocity *= 0                  # para

        if is_on_barrier(player2, track_image):
            player2.position -= player2.velocity
            player2.velocity *= 0

        # colisão entre jogadores
        resolve_collision(player1, player2)

        # desenho
        screen.blit(track_image, (0, 0))
        player1.draw(screen)
        player2.draw(screen)

        draw_exit_button(screen, font)

        pygame.display.flip()

    return "menu"