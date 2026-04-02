from __future__ import annotations

import pygame

from scenes.menu import Menu
from scenes.level_select import LevelSelect

from config import GameConfig
from phases import Phase1


class HorizontalRacingApp:
    def __init__(self, config: GameConfig | None = None):
        self.config = config or GameConfig()
        self.screen: pygame.Surface | None = None
        self.clock: pygame.time.Clock | None = None
        self.font = None
        self.small_font = None

    def run(self) -> int:
        pygame.init()
        self.screen = pygame.display.set_mode((self.config.width, self.config.height))
        pygame.display.set_caption(self.config.title)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 32)
        self.small_font = pygame.font.SysFont("Arial", 22)

        result = self._main_loop()
        pygame.quit()
        return result

    def _main_loop(self) -> int:
        assert self.screen is not None
        assert self.clock is not None

        menu = Menu(self.screen)
        level_select = self._build_level_select(self.screen)

        while True:
            option = menu.run()

            if option == "exit":
                return 0

            if option == "credits":
                self._show_simple_message("Créditos disponíveis no jogo principal.")
                continue

            if option == "settings":
                self._show_simple_message("Configurações ainda não implementadas.")
                continue

            if option != "start":
                continue

            selected_level = level_select.run()
            if selected_level == "menu":
                continue
            if selected_level == "exit":
                return 0

            if selected_level == 0:
                phase = Phase1(self.screen, self.clock, self.font, self.small_font)
                phase_result = phase.run()
                if phase_result == "exit":
                    return 0
            else:
                self._show_simple_message("Essa fase ainda nao foi implementada.")

    def _build_level_select(self, screen: pygame.Surface) -> LevelSelect:
        selector = LevelSelect(screen)
        selector.levels = [
            {"name": "Fase 1", "unlocked": True},
            {"name": "Fase 2", "unlocked": False},
            {"name": "Fase 3", "unlocked": False},
            {"name": "Fase 4", "unlocked": False},
            {"name": "Fase 5", "unlocked": False},
            {"name": "Fase 6", "unlocked": False},
            {"name": "Fase 7", "unlocked": False},
            {"name": "Fase 8", "unlocked": False},
            {"name": "Fase 9", "unlocked": False},
            {"name": "Fase 10", "unlocked": False},
        ]
        selector.selected = 0
        return selector

    def _show_simple_message(self, text: str, seconds: float = 1.4) -> None:
        assert self.screen is not None
        assert self.clock is not None

        timer = 0.0
        while timer < seconds:
            dt = self.clock.tick(self.config.fps) / 1000.0
            timer += dt

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            self.screen.fill((15, 15, 15))
            msg = self.small_font.render(text, True, (240, 240, 240))
            hint = self.small_font.render("ESC para voltar", True, (190, 190, 190))
            self.screen.blit(msg, (self.config.width // 2 - msg.get_width() // 2, self.config.height // 2 - 20))
            self.screen.blit(hint, (self.config.width // 2 - hint.get_width() // 2, self.config.height // 2 + 20))
            pygame.display.flip()
