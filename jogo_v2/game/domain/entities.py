from __future__ import annotations

from dataclasses import dataclass
import pygame


@dataclass
class Vec2:
    x: float = 0.0
    y: float = 0.0


class Car:
    ACCELERATION = 900.0
    FRICTION = 650.0
    MAX_SPEED = 340.0

    def __init__(self, x: float, y: float, size: int, color, controls, bounds_rect: pygame.Rect):
        self.position = Vec2(float(x), float(y))
        self.velocity = Vec2(0.0, 0.0)
        self.size = float(size)
        self.color = color
        self.controls = controls
        self.bounds_rect = bounds_rect

        self.has_shield = False
        

    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.position.x), int(self.position.y), int(self.size), int(self.size))

    def handle_input_and_move(self, dt: float, keys) -> None:
        input_x = 0.0
        input_y = 0.0

        if keys[self.controls["left"]]:
            input_x -= 1.0
        if keys[self.controls["right"]]:
            input_x += 1.0
        if keys[self.controls["up"]]:
            input_y -= 1.0
        if keys[self.controls["down"]]:
            input_y += 1.0

        self._update_axis(dt, input_x, "x")
        self._update_axis(dt, input_y, "y")

        self.velocity.x = max(-self.MAX_SPEED, min(self.MAX_SPEED, self.velocity.x))
        self.velocity.y = max(-self.MAX_SPEED, min(self.MAX_SPEED, self.velocity.y))

        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt
        self._clamp_to_bounds()

    def _update_axis(self, dt: float, input_value: float, axis: str) -> None:
        current = getattr(self.velocity, axis)
        if input_value != 0.0:
            current += input_value * self.ACCELERATION * dt
        else:
            friction = self.FRICTION * dt
            if abs(current) <= friction:
                current = 0.0
            else:
                current -= friction * (1 if current > 0 else -1)
        setattr(self.velocity, axis, current)

    def _clamp_to_bounds(self) -> None:
        min_x = self.bounds_rect.left
        max_x = self.bounds_rect.right - self.size
        min_y = self.bounds_rect.top
        max_y = self.bounds_rect.bottom - self.size

        if self.position.x < min_x:
            self.position.x = float(min_x)
            self.velocity.x = 0.0
        if self.position.x > max_x:
            self.position.x = float(max_x)
            self.velocity.x = 0.0
        if self.position.y < min_y:
            self.position.y = float(min_y)
            self.velocity.y = 0.0
        if self.position.y > max_y:
            self.position.y = float(max_y)
            self.velocity.y = 0.0

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.color, self.rect(), border_radius=6)
        head = pygame.Rect(
            int(self.position.x + self.size - 8),
            int(self.position.y + 6),
            6,
            int(self.size - 12),
        )
        pygame.draw.rect(screen, (255, 255, 255), head, border_radius=3)


class Obstacle:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        speed,
        color=(40,40,40)
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.speed = speed
        
    def update(self, dt):
        self.rect.x -= int(self.speed * dt)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.color, self.rect, border_radius=4)

class Item:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        speed,
        effect,
        color=(0, 255, 0)
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.effect = effect
        
        if effect == "speed":
            self.color = (0, 180, 255)      # Azul
        elif effect == "shield":
            self.color = (0, 255, 0)        # Verde
        else:
            self.color = (255, 255, 255)    # Branco

    def update(self, dt):
        self.rect.x -= int(self.speed * dt)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=4)