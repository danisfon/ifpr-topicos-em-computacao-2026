from __future__ import annotations

import pygame


class Animation:
    """Sequência de sprites, avançada pelo tempo em segundos."""

    def __init__(self, sprites: list[pygame.Surface], fps: float = 8.0, loop: bool = True):
        if not sprites or fps <= 0.0:
            raise ValueError("Uma animação precisa de sprites e FPS positivo")
        self.sprites = list(sprites)
        self.fps = float(fps)
        self.loop = loop
        self.elapsed = 0.0

    def update(self, dt: float) -> None:
        self.elapsed += max(0.0, dt)

    def reset(self) -> None:
        self.elapsed = 0.0

    @property
    def frame(self) -> pygame.Surface:
        index = int(self.elapsed * self.fps)
        index = index % len(self.sprites) if self.loop else min(index, len(self.sprites) - 1)
        return self.sprites[index]


class AnimationSet:
    """Cada objeto tem seu conjunto e seu próprio relógio de animação."""

    def __init__(self, animations: dict[str, Animation], initial: str):
        self.animations = animations
        self.current = initial

    def play(self, name: str) -> None:
        if name not in self.animations:
            raise KeyError(name)
        if name != self.current:
            self.current = name
            self.animations[name].reset()

    def update(self, dt: float) -> None:
        self.animations[self.current].update(dt)

    @property
    def frame(self) -> pygame.Surface:
        return self.animations[self.current].frame


def driving_frames(image: pygame.Surface) -> list[pygame.Surface]:
    """Reaproveita a arte do carro em quadros de vibração da suspensão."""
    frames = []
    for offset in (0, -1, 0, 1):
        frame = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        frame.blit(image, (0, offset))
        frames.append(frame)
    return frames
