from __future__ import annotations

from pathlib import Path

import pygame

from ..core.config import P1_CONTROLS, P2_CONTROLS
from ..domain.entities import Car
from ..domain.gameWorld import PlayerLane

_SPRITES_DIR = Path(__file__).resolve().parents[2] / "assets" / "sprites"
_SOUNDS_DIR  = Path(__file__).resolve().parents[2] / "assets" / "sounds"


class GameManager:
    PHASE_NAME     = "Fase 1"
    CAR_MAX_WIDTH  = 70
    CAR_MAX_HEIGHT = 100

    def __init__(
        self,
        screen: pygame.Surface,
        clock: pygame.time.Clock,
        font,
        small_font,
    ) -> None:
        self.screen     = screen
        self.clock      = clock
        self.font       = font
        self.small_font = small_font

        self.width  = screen.get_width()
        self.height = screen.get_height()

        self._music_started = False

        self.p1, self.p2 = self._create_players()

    def run(self) -> str:
        self._start_music()

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
                self._draw_global_hud()

                pygame.display.flip()

        finally:
            self._stop_music()

    @property
    def is_game_over(self) -> bool:
        return (not self.p1.alive) and (not self.p2.alive)

    def _create_players(self) -> tuple[PlayerLane, PlayerLane]:
        margin      = 12
        lane_height = (self.height - 100) // 2

        track1 = pygame.Rect(20, 80,                        self.width - 40, lane_height - margin)
        track2 = pygame.Rect(20, 80 + lane_height + margin, self.width - 40, lane_height - margin)

        p1_car = self._build_car(track1, P1_CONTROLS, "playerBranco.png", "playerBrancoDanificado.png")
        p2_car = self._build_car(track2, P2_CONTROLS, "playerBranco.png", "playerBrancoDanificado.png")

        p1 = PlayerLane("Jogador 1", track1, p1_car, (255, 255, 255))
        p2 = PlayerLane("Jogador 2", track2, p2_car, (255, 255, 255))

        return p1, p2

    def _build_car(
        self,
        track: pygame.Rect,
        controls: dict,
        sprite_name: str,
        damaged_sprite_name: str,
    ) -> Car:
        return Car(
            x=float(track.left + 90),
            y=float(track.centery - self.CAR_MAX_HEIGHT // 2),
            max_width=self.CAR_MAX_WIDTH,
            max_height=self.CAR_MAX_HEIGHT,
            sprite_path=str(_SPRITES_DIR / sprite_name),
            damaged_sprite_path=str(_SPRITES_DIR / damaged_sprite_name),
            controls=controls,
            bounds_rect=track,
        )

    def _draw_global_hud(self) -> None:
        self._draw_header()
        if self.is_game_over:
            self._draw_game_over_panel()

    def _draw_header(self) -> None:
        title = self.font.render(
            f"Corrida Horizontal de Sobrevivência — {self.PHASE_NAME}",
            True, (255, 255, 255),
        )
        controls = self.small_font.render(
            "P1: WASD  |  P2: Setas  |  ESC: Menu  |  R: Reiniciar",
            True, (220, 220, 220),
        )

        self.screen.blit(title,    (self.width // 2 - title.get_width()    // 2, 8))
        self.screen.blit(controls, (self.width // 2 - controls.get_width() // 2, 44))

    def _draw_game_over_panel(self) -> None:
        if self.p1.survival_time > self.p2.survival_time:
            result_text = "Vencedor: Jogador 1"
            color = self.p1.accent_color
        elif self.p2.survival_time > self.p1.survival_time:
            result_text = "Vencedor: Jogador 2"
            color = self.p2.accent_color
        else:
            result_text = "Empate!"
            color = (255, 255, 255)

        panel = pygame.Rect(self.width // 2 - 240, self.height // 2 - 75, 480, 150)
        bg = pygame.Surface((panel.width, panel.height), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 185))
        self.screen.blit(bg, panel.topleft)
        pygame.draw.rect(self.screen, color, panel, 3, border_radius=8)

        result_surf  = self.font.render(result_text, True, color)
        detail_surf  = self.small_font.render(
            f"J1: {self.p1.survival_time:.2f}s  |  J2: {self.p2.survival_time:.2f}s",
            True, (240, 240, 240),
        )
        restart_surf = self.small_font.render(
            "Pressione R para jogar novamente", True, (255, 255, 255),
        )

        cx = panel.centerx
        self.screen.blit(result_surf,  (cx - result_surf.get_width()  // 2, panel.y + 20))
        self.screen.blit(detail_surf,  (cx - detail_surf.get_width()  // 2, panel.y + 65))
        self.screen.blit(restart_surf, (cx - restart_surf.get_width() // 2, panel.y + 100))

    def _start_music(self) -> None:
        if self._music_started:
            return

        mp3_files = sorted(_SOUNDS_DIR.glob("*.mp3"))
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
            pass

    def _stop_music(self) -> None:
        if self._music_started and pygame.mixer.get_init():
            pygame.mixer.music.stop()
        self._music_started = False


class Phase1(GameManager):
    pass