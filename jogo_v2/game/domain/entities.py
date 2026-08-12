

from __future__ import annotations

from dataclasses import dataclass
import pygame


@dataclass
class Vec2:
    x: float = 0.0
    y: float = 0.0


class Sprite:
    def __init__(self, sprite_path: str, width: int, height: int):
        self.surface = self._load_scaled(sprite_path, width, height)

    def _load_scaled(self, sprite_path: str, width: int, height: int) -> pygame.Surface:
        sprite = pygame.image.load(sprite_path).convert_alpha()
        bounding = sprite.get_bounding_rect()

        if bounding.width and bounding.height:
            sprite = sprite.subsurface(bounding)

        original_width = sprite.get_width()
        original_height = sprite.get_height()

        if original_width == 0 or original_height == 0:
            return sprite

        scale = min(width / original_width, height / original_height)
        new_width = max(1, int(original_width * scale))
        new_height = max(1, int(original_height * scale))

        return pygame.transform.smoothscale(sprite, (new_width, new_height))


class GameObject:
    def __init__(self, x: float, y: float, width: int, height: int, sprite_path: str):
        self.position = Vec2(float(x), float(y))
        self.sprite = Sprite(sprite_path, width, height)
        self.width = self.sprite.surface.get_width()
        self.height = self.sprite.surface.get_height()

    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.position.x), int(self.position.y), self.width, self.height)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.sprite.surface, (self.position.x, self.position.y))


class StaticObject(GameObject):
    pass


class DynamicObject(GameObject):
    def __init__(self, x: float, y: float, width: int, height: int, sprite_path: str):
        super().__init__(x, y, width, height, sprite_path)
        self.velocity = Vec2(0.0, 0.0)
        self.acceleration = Vec2(0.0, 0.0)

    def update_motion(self, dt: float) -> None:
        self.velocity.x += self.acceleration.x * dt
        self.velocity.y += self.acceleration.y * dt
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt


class Car(DynamicObject):
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
        super().__init__(x, y, width, height, sprite_path)
        self.controls = controls
        self.bounds_rect = bounds_rect
        self.has_shield = False
        self.damaged = False
        self.damaged_sprite = Sprite(damaged_sprite_path, width, height).surface

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

        self.acceleration.x = input_x * self.ACCELERATION
        self.acceleration.y = input_y * self.ACCELERATION

        self.update_motion(dt)
        self._apply_friction(dt, input_x, "x")
        self._apply_friction(dt, input_y, "y")
        self._clamp_speed()
        self._clamp_to_bounds()

    def _apply_friction(self, dt: float, input_value: float, axis: str) -> None:
        if input_value != 0.0:
            return

        current = getattr(self.velocity, axis)
        friction = self.FRICTION * dt

        if abs(current) <= friction:
            current = 0.0
        else:
            current -= friction * (1 if current > 0 else -1)

        setattr(self.velocity, axis, current)

    def _clamp_speed(self) -> None:
        self.velocity.x = max(-self.MAX_SPEED, min(self.MAX_SPEED, self.velocity.x))
        self.velocity.y = max(-self.MAX_SPEED, min(self.MAX_SPEED, self.velocity.y))

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
        sprite = self.damaged_sprite if self.damaged else self.sprite.surface
        if sprite is None:
            sprite = self.sprite.surface
        screen.blit(sprite, (self.position.x, self.position.y))


class Obstacle(DynamicObject):
    def __init__(self, x, y, width, height, speed, sprite_path, acceleration_x: float = 0.0):
        super().__init__(x, y, width, height, sprite_path)
        self.velocity.x = -float(speed)
        self.acceleration.x = float(acceleration_x)

    def update(self, dt):
        self.update_motion(dt)


class Consumable(DynamicObject):
    def __init__(self, x, y, width, height, speed, effect, sprite_path):
        super().__init__(x, y, width, height, sprite_path)
        self.velocity.x = -float(speed)
        self.effect = effect

    def update(self, dt):
        self.update_motion(dt)


class Item(Consumable):
    pass