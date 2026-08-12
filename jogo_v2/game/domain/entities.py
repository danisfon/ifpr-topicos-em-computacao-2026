from __future__ import annotations

from dataclasses import dataclass
import pygame


@dataclass
class Vec2:
    x: float = 0.0
    y: float = 0.0

    def __add__(self, other: Vec2) -> Vec2:
        return Vec2(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float) -> Vec2:
        return Vec2(self.x * scalar, self.y * scalar)


class Sprite:
    def __init__(self, sprite_path: str, max_width: int, max_height: int) -> None:
        self.surface: pygame.Surface = self._load_scaled(sprite_path, max_width, max_height)

    def _load_scaled(self, path: str, max_width: int, max_height: int) -> pygame.Surface:
        image = pygame.image.load(path).convert_alpha()

        bounding = image.get_bounding_rect()
        if bounding.width > 0 and bounding.height > 0:
            image = image.subsurface(bounding)

        orig_w = image.get_width()
        orig_h = image.get_height()

        if orig_w == 0 or orig_h == 0:
            return image

        scale = min(max_width / orig_w, max_height / orig_h)
        new_w = max(1, int(orig_w * scale))
        new_h = max(1, int(orig_h * scale))

        return pygame.transform.smoothscale(image, (new_w, new_h))

    @property
    def width(self) -> int:
        return self.surface.get_width()

    @property
    def height(self) -> int:
        return self.surface.get_height()


class GameObject:
    def __init__(self, x: float, y: float, max_width: int, max_height: int, sprite_path: str) -> None:
        self.position = Vec2(float(x), float(y))
        self.sprite = Sprite(sprite_path, max_width, max_height)

    @property
    def width(self) -> int:
        return self.sprite.width

    @property
    def height(self) -> int:
        return self.sprite.height

    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.position.x), int(self.position.y), self.width, self.height)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.sprite.surface, (self.position.x, self.position.y))

    def update(self, dt: float) -> None:
        pass


class StaticObject(GameObject):
    pass


class DynamicObject(GameObject):
    def __init__(self, x: float, y: float, max_width: int, max_height: int, sprite_path: str) -> None:
        super().__init__(x, y, max_width, max_height, sprite_path)
        self.velocity = Vec2(0.0, 0.0)
        self.acceleration = Vec2(0.0, 0.0)

    def update_motion(self, dt: float) -> None:
        self.velocity.x += self.acceleration.x * dt
        self.velocity.y += self.acceleration.y * dt
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt


class Car(DynamicObject):
    ACCELERATION: float = 900.0
    FRICTION: float = 650.0
    MAX_SPEED: float = 340.0

    def __init__(
        self,
        x: float,
        y: float,
        max_width: int,
        max_height: int,
        sprite_path: str,
        damaged_sprite_path: str,
        controls: dict,
        bounds_rect: pygame.Rect,
    ) -> None:
        super().__init__(x, y, max_width, max_height, sprite_path)
        self.controls = controls
        self.bounds_rect = bounds_rect.copy()
        self.has_shield = False
        self.damaged = False
        self._damaged_sprite = Sprite(damaged_sprite_path, max_width, max_height)

    def update(self, dt: float, keys) -> None:
        input_x, input_y = self._read_input(keys)

        self.acceleration.x = input_x * self.ACCELERATION
        self.acceleration.y = input_y * self.ACCELERATION

        self.update_motion(dt)
        self._apply_friction(dt, input_x, "x")
        self._apply_friction(dt, input_y, "y")
        self._clamp_speed()
        self._clamp_to_bounds()

    def _read_input(self, keys) -> tuple[float, float]:
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

        return input_x, input_y

    def _apply_friction(self, dt: float, input_value: float, axis: str) -> None:
        if input_value != 0.0:
            return

        current = getattr(self.velocity, axis)
        reduction = self.FRICTION * dt

        if abs(current) <= reduction:
            current = 0.0
        else:
            current -= reduction * (1.0 if current > 0.0 else -1.0)

        setattr(self.velocity, axis, current)

    def _clamp_speed(self) -> None:
        self.velocity.x = max(-self.MAX_SPEED, min(self.MAX_SPEED, self.velocity.x))
        self.velocity.y = max(-self.MAX_SPEED, min(self.MAX_SPEED, self.velocity.y))

    def _clamp_to_bounds(self) -> None:
        min_x = float(self.bounds_rect.left)
        max_x = float(self.bounds_rect.right - self.width)
        min_y = float(self.bounds_rect.top)
        max_y = float(self.bounds_rect.bottom - self.height)

        if self.position.x < min_x:
            self.position.x = min_x
            self.velocity.x = 0.0

        if self.position.x > max_x:
            self.position.x = max_x
            self.velocity.x = 0.0

        if self.position.y < min_y:
            self.position.y = min_y
            self.velocity.y = 0.0

        if self.position.y > max_y:
            self.position.y = max_y
            self.velocity.y = 0.0

    def draw(self, screen: pygame.Surface) -> None:
        surface = self._damaged_sprite.surface if self.damaged else self.sprite.surface
        screen.blit(surface, (self.position.x, self.position.y))


class Obstacle(DynamicObject):
    def __init__(
        self,
        x: float,
        y: float,
        max_width: int,
        max_height: int,
        speed: float,
        sprite_path: str,
        acceleration_x: float = 0.0,
    ) -> None:
        super().__init__(x, y, max_width, max_height, sprite_path)
        self.velocity.x = -float(speed)
        self.acceleration.x = float(acceleration_x)

    def update(self, dt: float) -> None:
        self.update_motion(dt)
        # garante que o obstáculo nunca ande para a direita
        if self.velocity.x > 0.0:
            self.velocity.x = 0.0

class Consumable(DynamicObject):
    def __init__(
        self,
        x: float,
        y: float,
        max_width: int,
        max_height: int,
        speed: float,
        effect: str,
        sprite_path: str,
    ) -> None:
        super().__init__(x, y, max_width, max_height, sprite_path)
        self.velocity.x = -float(speed)
        self.effect = effect

    def update(self, dt: float) -> None:
        self.update_motion(dt)


class Item(Consumable):
    pass