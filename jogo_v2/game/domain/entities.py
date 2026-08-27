

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

    def __init__(
        self,
        x: float,
        y: float,
        width: int,
        height: int,
        sprite_path: str,
        damaged_sprite_path: str,
        controls,
        bounds_rect: pygame.Rect,
    ):
        self.position = Vec2(float(x), float(y))
        self.velocity = Vec2(0.0, 0.0)

        self.width = width
        self.height = height

        self.controls = controls
        self.bounds_rect = bounds_rect

        self.has_shield = False
        self.damaged = False

        self.sprite = self._load_sprite(sprite_path)
        self.damaged_sprite = self._load_sprite(damaged_sprite_path)

        # Guarda o tamanho real da sprite normal
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()

    def _load_sprite(self, sprite_path):
        sprite = pygame.image.load(sprite_path).convert_alpha()

        # Remove bordas transparentes
        bounding = sprite.get_bounding_rect()

        if not bounding.width or not bounding.height:
            return sprite

        sprite = sprite.subsurface(bounding)

        # Mantém a proporção da imagem
        original_width = sprite.get_width()
        original_height = sprite.get_height()

        scale = min(
            self.width / original_width,
            self.height / original_height
        )

        new_width = int(original_width * scale)
        new_height = int(original_height * scale)

        sprite = pygame.transform.smoothscale(
            sprite,
            (new_width, new_height)
        )

        return sprite

    def rect(self) -> pygame.Rect:
        return pygame.Rect(
            int(self.position.x),
            int(self.position.y),
            self.width,
            self.height,
        )

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
        max_x = self.bounds_rect.right - self.width

        min_y = self.bounds_rect.top
        max_y = self.bounds_rect.bottom - self.height

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

        if self.damaged:
            sprite = self.damaged_sprite
        else:
            sprite = self.sprite

        screen.blit(
            sprite,
            (self.position.x, self.position.y),
        )


class Obstacle:

    def __init__(
        self,
        x,
        y,
        width,
        height,
        speed,
        sprite_path,
    ):
        self.rect = pygame.Rect(
            x,
            y,
            width,
            height,
        )

        self.speed = speed

        self.sprite = pygame.image.load(sprite_path).convert_alpha()

        # Remove as bordas transparentes da imagem
        bounding = self.sprite.get_bounding_rect()
        self.sprite = self.sprite.subsurface(bounding)

        # Mantém a proporção da sprite
        original_width = self.sprite.get_width()
        original_height = self.sprite.get_height()

        scale = min(
            width / original_width,
            height / original_height
        )

        new_width = int(original_width * scale)
        new_height = int(original_height * scale)

        self.sprite = pygame.transform.smoothscale(
            self.sprite,
            (new_width, new_height)
        )

        # Atualiza o tamanho real da colisão
        self.rect = pygame.Rect(
            x,
            y,
            new_width,
            new_height,
        )

    def update(self, dt):
        self.rect.x -= int(self.speed * dt)

    def draw(self, screen):
        screen.blit(
            self.sprite,
            self.rect,
        )


class Item:

    def __init__(
        self,
        x,
        y,
        width,
        height,
        speed,
        effect,
        sprite_path,
    ):
        self.rect = pygame.Rect(
            x,
            y,
            width,
            height,
        )

        self.speed = speed
        self.effect = effect

        self.sprite = pygame.image.load(sprite_path).convert_alpha()

        bounding = self.sprite.get_bounding_rect()
        self.sprite = self.sprite.subsurface(bounding)

        self.sprite = pygame.transform.smoothscale(
            self.sprite,
            (width, height)
        )


    def update(self, dt):
        self.rect.x -= int(self.speed * dt)

    def draw(self, screen):
        screen.blit(self.sprite, self.rect)