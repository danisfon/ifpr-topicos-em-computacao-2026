from __future__ import annotations

from pathlib import Path
import pygame

from ..core.config import P1_CONTROLS, P2_CONTROLS
from ..domain.entities import Car
from ..domain.player_lane import PlayerLane


class Phase1:
    name = "Fase 1"

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, font, small_font):
        self.screen = screen
        self.clock = clock
        self.font = font
        self.small_font = small_font

        self.width = screen.get_width()
        self.height = screen.get_height()
        self._music_started = False

        self.p1, self.p2 = self._create_players()

    def run(self) -> str:
        self._start_phase_music()
        try:
            while True:
                dt = self.clock.tick(60) / 1000.0

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return "exit"
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            return "menu"
                        if event.key == pygame.K_r and self.is_game_over:
                            self.p1, self.p2 = self._create_players()

                keys = pygame.key.get_pressed()
                self.p1.update(dt, keys)
                self.p2.update(dt, keys)

                self.screen.fill((22, 22, 24))
                self.p1.draw(self.screen, self.font, self.small_font)
                self.p2.draw(self.screen, self.font, self.small_font)
                self._draw_ui()
                pygame.display.flip()
        finally:
            self._stop_phase_music()

    @property
    def is_game_over(self) -> bool:
        return (not self.p1.alive) and (not self.p2.alive)

    def _create_players(self):
        margin = 12
        lane_height = (self.height - 100) // 2

        track1 = pygame.Rect(20, 80, self.width - 40, lane_height - margin)
        track2 = pygame.Rect(20, 80 + lane_height + margin, self.width - 40, lane_height - margin)

        p1_car = Car(track1.left + 90, track1.centery - 18, 36, (170, 70, 255), P1_CONTROLS, track1)
        p2_car = Car(track2.left + 90, track2.centery - 18, 36, (255, 80, 80), P2_CONTROLS, track2)

        p1 = PlayerLane("Jogador 1", track1, p1_car, (190, 120, 255))
        p2 = PlayerLane("Jogador 2", track2, p2_car, (255, 120, 120))
        return p1, p2

    def _draw_ui(self) -> None:
        title = self.font.render("Corrida Horizontal de Sobrevivência - Fase 1", True, (255, 255, 255))
        controls = self.small_font.render(
            "P1: WASD | P2: Setas | ESC: Menu | R: Reiniciar",
            True,
            (230, 230, 230),
        )

        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 8))
        self.screen.blit(controls, (self.width // 2 - controls.get_width() // 2, 44))

        if self.is_game_over:
            if self.p1.survival_time > self.p2.survival_time:
                result = "Vencedor: Jogador 1"
                color = self.p1.accent_color
            elif self.p2.survival_time > self.p1.survival_time:
                result = "Vencedor: Jogador 2"
                color = self.p2.accent_color
            else:
                result = "Empate"
                color = (255, 255, 255)

            panel = pygame.Rect(self.width // 2 - 230, self.height // 2 - 70, 460, 140)
            bg = pygame.Surface((panel.width, panel.height), pygame.SRCALPHA)
            bg.fill((0, 0, 0, 180))
            self.screen.blit(bg, panel.topleft)
            pygame.draw.rect(self.screen, color, panel, 3, border_radius=8)

            result_text = self.font.render(result, True, color)
            detail = self.small_font.render(
                f"J1: {self.p1.survival_time:.2f}s  |  J2: {self.p2.survival_time:.2f}s",
                True,
                (240, 240, 240),
            )
            restart = self.small_font.render("Pressione R para jogar novamente", True, (255, 255, 255))

            self.screen.blit(result_text, (panel.centerx - result_text.get_width() // 2, panel.y + 22))
            self.screen.blit(detail, (panel.centerx - detail.get_width() // 2, panel.y + 62))
            self.screen.blit(restart, (panel.centerx - restart.get_width() // 2, panel.y + 92))

    def _start_phase_music(self) -> None:
        if self._music_started:
            return

        sounds_dir = Path(__file__).resolve().parents[2] / "assets" / "sounds"
        mp3_files = sorted(sounds_dir.glob("*.mp3"))
        if not mp3_files:
            return

        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init()
            except pygame.error:
                return

        try:
            pygame.mixer.music.load(str(mp3_files[0]))
            pygame.mixer.music.set_volume(0.45)
            pygame.mixer.music.play(-1)
            self._music_started = True
        except pygame.error:
            self._music_started = False

    def _stop_phase_music(self) -> None:
        if not self._music_started:
            return

        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
        self._music_started = False
