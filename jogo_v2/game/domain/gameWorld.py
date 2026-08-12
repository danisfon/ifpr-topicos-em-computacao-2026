from __future__ import annotations

import random
from pathlib import Path
import pygame

from .collision import CollisionManager
from .entities import Car, Obstacle, Consumable


class GameWorld:

    OBSTACLE_WIDTH = 70
    OBSTACLE_HEIGHT = 100

    def __init__(self, name: str, track_rect: pygame.Rect, car: Car, accent_color):
        self.name = name
        self.track_rect = track_rect.copy()
        self.car = car
        self.accent_color = accent_color

        self.alive = True
        self.survival_time = 0.0

        self.obstacles: list[Obstacle] = []
        self.items: list[Consumable] = []

        self.spawn_timer = 0.0
        self.item_spawn_timer = 3.0
        self.lane_offset = 0.0
        self.speed_boost_timer = 0.0

        # Pasta onde ficam os carros dos obstáculos
        sprites_path = (
            Path(__file__).resolve().parents[2]
            / "assets"
            / "sprites"
        )

        self.obstacle_sprites = [
            str(sprites_path / "obstaculo.png"),
            str(sprites_path / "obstaculo2.png"),
        ]

    def current_world_speed(self) -> float:
        return 220.0 + min(220.0, self.survival_time * 14.0)

    def update(self, dt: float, keys) -> None:

        if not self.alive:
            return

        self.survival_time += dt
        self._update_effects(dt)

        self.lane_offset += self.current_world_speed() * dt

        self.car.handle_input_and_move(dt, keys)

        self.spawn_timer -= dt

        if self.spawn_timer <= 0:

            self._spawn_obstacle()

            dynamic = max(
                0.0,
                0.55 - self.survival_time * 0.02,
            )

            self.spawn_timer = random.uniform(
                0.28 + dynamic,
                0.9 + dynamic,
            )

        for obstacle in self.obstacles:
            obstacle.update(dt)

        self.obstacles = [
            o
            for o in self.obstacles
            if o.rect().right > self.track_rect.left - 40
        ]

        self.item_spawn_timer -= dt

        if self.item_spawn_timer <= 0:
            self._spawn_item()
            self.item_spawn_timer = random.uniform(3.0, 6.0)

        for item in self.items:
            item.update(dt)

        self.items = [
            item
            for item in self.items
            if item.rect().right > self.track_rect.left - 40
        ]

        hit_obstacle, consumed_items, collided_obstacle = CollisionManager.resolve_basic(self.car, self.obstacles, self.items)

        if hit_obstacle:
            if self.car.has_shield:
                self.car.has_shield = False
                if collided_obstacle is not None and collided_obstacle in self.obstacles:
                    self.obstacles.remove(collided_obstacle)
            else:
                self.car.damaged = True
                self.alive = False

        for consumed in consumed_items:
            self._apply_consumable(consumed.effect)

    def _spawn_obstacle(self):

        x = self.track_rect.right + random.randint(0, 260)

        y = random.randint(
            self.track_rect.top + 8,
            self.track_rect.bottom - self.OBSTACLE_HEIGHT - 8,
        )

        speed = random.randint(180, 580)
        acceleration_x = random.uniform(-30.0, 30.0)

        sprite = random.choice(self.obstacle_sprites)

        self.obstacles.append(
            Obstacle(
                x=x,
                y=y,
                width=self.OBSTACLE_WIDTH,
                height=self.OBSTACLE_HEIGHT,
                speed=speed,
                acceleration_x=acceleration_x,
                sprite_path=sprite,
            )
        )

    def _spawn_item(self):

        width = 24
        height = 24

        x = self.track_rect.right + random.randint(0, 260)

        y = random.randint(
            self.track_rect.top + 8,
            self.track_rect.bottom - height - 8,
        )

        speed = random.randint(180, 350)

        sprites_path = (
            Path(__file__).resolve().parents[2]
            / "assets"
            / "sprites"
        )

        effect = random.choice(["speed", "shield", "stability"])

        if effect in ("speed", "stability"):
            sprite = str(sprites_path / "speed.png")
        else:
            sprite = str(sprites_path / "shield.png")

        self.items.append(
            Gameble(
                x,
                y,
                width,
                height,
                speed,
                effect,
                sprite
            )
        )

    def draw(self, screen: pygame.Surface, font, small_font) -> None:

        pygame.draw.rect(
            screen,
            (70, 70, 70),
            self.track_rect,
        )

        pygame.draw.rect(
            screen,
            self.accent_color,
            self.track_rect,
            3,
        )

        self._draw_lane_stripes(screen)

        for item in self.items:
            item.draw(screen)

        for obstacle in self.obstacles:
            obstacle.draw(screen)

        self.car.draw(screen)

        name_text = font.render(
            self.name,
            True,
            self.accent_color,
        )

        time_text = small_font.render(
            f"Tempo: {self.survival_time:.2f}s",
            True,
            (255, 255, 255),
        )

        status_color = (
            (120, 255, 120)
            if self.alive
            else (255, 120, 120)
        )

        status_text = small_font.render(
            "VIVO" if self.alive else "ELIMINADO",
            True,
            status_color,
        )

        screen.blit(
            name_text,
            (self.track_rect.left + 10, self.track_rect.top + 8),
        )

        screen.blit(
            time_text,
            (self.track_rect.left + 10, self.track_rect.top + 42),
        )

        screen.blit(
            status_text,
            (self.track_rect.left + 10, self.track_rect.top + 64),
        )

    def _draw_lane_stripes(self, screen):

        stripe_y = self.track_rect.centery

        stripe_w = 40
        gap = 30

        offset = int(
            self.lane_offset % (stripe_w + gap)
        )

        x = self.track_rect.left - offset

        while x < self.track_rect.right:

            pygame.draw.rect(
                screen,
                (220, 220, 220),
                (
                    x,
                    stripe_y - 4,
                    stripe_w,
                    8,
                ),
                border_radius=3,
            )

            x += stripe_w + gap

    def _apply_consumable(self, effect: str) -> None:
        if effect == "speed":
            self.car.MAX_SPEED += 30
            self.speed_boost_timer = 3.5
            return

        if effect == "shield":
            self.car.has_shield = True
            return

        if effect == "stability":
            self.car.FRICTION = min(900.0, self.car.FRICTION + 80.0)

    def _update_effects(self, dt: float) -> None:
        if self.speed_boost_timer > 0.0:
            self.speed_boost_timer -= dt
            if self.speed_boost_timer <= 0.0:
                self.car.MAX_SPEED = max(340.0, self.car.MAX_SPEED - 30)


class PlayerLane(GameWorld):
    pass