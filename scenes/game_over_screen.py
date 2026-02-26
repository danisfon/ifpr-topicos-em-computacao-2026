import pygame
from setting import SCREEN_WIDTH, SCREEN_HEIGHT

class GameOverScreen:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()

        self.font_big = pygame.font.SysFont("Arial", 50, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 25, bold=True)

    def run(self, final_time_text, winner_text=None):
        """Mostra a tela final até o jogador sair (ESC/Enter ou fechar)."""
        running_end = True

        while running_end:
            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running_end = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                        running_end = False

            self.screen.fill((0, 0, 0))

            title = self.font_big.render("FIM DE JOGO", True, (255, 255, 255))
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 80))
            self.screen.blit(title, title_rect)

            if winner_text:
                winner = self.font_small.render(winner_text, True, (255, 255, 255))
                winner_rect = winner.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 25))
                self.screen.blit(winner, winner_rect)

            time_msg = self.font_small.render(f"Tempo total: {final_time_text}", True, (255, 255, 255))
            time_rect = time_msg.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
            self.screen.blit(time_msg, time_rect)

            hint = self.font_small.render("ESC ou Enter para sair", True, (180, 180, 180))
            hint_rect = hint.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 70))
            self.screen.blit(hint, hint_rect)

            pygame.display.flip()