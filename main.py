import pygame
from setting import *
from entities.player import Player
from scenes.game_over_screen import GameOverScreen

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    start_time = pygame.time.get_ticks()
    font = pygame.font.SysFont("Arial", 38, bold=True)

    clock = pygame.time.Clock()

    game_over_screen = GameOverScreen(screen)
    final_time_text = None
    winner_text = None

    # 🎮 Controles
    controls_player1 = {
        "left": pygame.K_a,
        "right": pygame.K_d,
        "up": pygame.K_w,
        "down": pygame.K_s
    }


    controls_player2 = {
        "left": pygame.K_LEFT,
        "right": pygame.K_RIGHT,
        "up": pygame.K_UP,
        "down": pygame.K_DOWN
    }

    #definindo 1. posicao 2. tamanho 3. velocidade 4. controle proprio 5. cor
    player1 = Player(100, 100, 50, 10, controls_player1, (160, 32, 230))
    player2 = Player(300, 300, 50, 10, controls_player2, (255, 0, 0))


    running = True
    while running:
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player1.handle_input()
        player2.handle_input()

        # updates (cooldown)
        player1.update()
        player2.update()

        # colisão entre jogadores
        if player1.get_rect().colliderect(player2.get_rect()):
            player1.take_hit(10)
            player2.take_hit(10)

            # “knockback” simples (empurra pra separar)
            dx = (player1.x + player1.w/2) - (player2.x + player2.w/2)
            dy = (player1.y + player1.h/2) - (player2.y + player2.h/2)

            # empurra no eixo dominante
            if abs(dx) > abs(dy):
                if dx > 0:
                    player1.x += 10
                    player2.x -= 10
                else:
                    player1.x -= 10
                    player2.x += 10
            else:
                if dy > 0:
                    player1.y += 10
                    player2.y -= 10
                else:
                    player1.y -= 10
                    player2.y += 10

        screen.fill((0, 0, 0))
        player1.draw(screen)
        player2.draw(screen)

        if player1.health == 0 or player2.health == 0:
            end_ms = pygame.time.get_ticks() - start_time

            minutes = end_ms // 60000
            seconds = (end_ms % 60000) // 1000
            milliseconds = end_ms % 1000
            final_time_text = f"{minutes:02}:{seconds:02}:{milliseconds:03}"

            # opcional: definir vencedor
            if player1.health == 0 and player2.health > 0:
                winner_text = "Vencedor: Jogador 2"
            elif player2.health == 0 and player1.health > 0:
                winner_text = "Vencedor: Jogador 1"
            else:
                winner_text = "Empate!"

            running = False

        # parte do cronômetro
        elapsed_ms = pygame.time.get_ticks() - start_time
        elapsed_seconds = elapsed_ms // 1000

        minutes = elapsed_seconds // 60
        seconds = elapsed_seconds % 60
        milliseconds = elapsed_ms % 1000
        time_text = f"{minutes:02}:{seconds:02}:{milliseconds:03}"

        timer_surface = font.render(time_text, True, (255, 255, 255))
        timer_surface.set_alpha(150) #opacidade
        timer_rect = timer_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(timer_surface, timer_rect)

        pygame.display.flip()

        if player1.health == 0 or player2.health == 0:
            running = False

    if final_time_text is not None:
        game_over_screen.run(final_time_text, winner_text)

    pygame.quit()


if __name__ == "__main__":
    main()
