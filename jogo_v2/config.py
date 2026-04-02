from dataclasses import dataclass
import pygame


@dataclass(frozen=True)
class GameConfig:
    width: int = 1280
    height: int = 720
    fps: int = 60
    title: str = "Corrida Horizontal de Sobrevivência"


P1_CONTROLS = {
    "left": pygame.K_a,
    "right": pygame.K_d,
    "up": pygame.K_w,
    "down": pygame.K_s,
}

P2_CONTROLS = {
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
}
