from __future__ import annotations

import random
from pathlib import Path

import pygame

from .collision import CollisionManager
from .entities import Car, Obstacle, Consumable
from .weapons import Weapon

_SPRITES_DIR = Path(__file__).resolve().parents[2] / "assets" / "sprites"


class GameWorld:
    OBSTACLE_WIDTH  = 70
    OBSTACLE_HEIGHT = 100
    ITEM_WIDTH      = 28
    ITEM_HEIGHT     = 28
    COIN_SIZE       = 32
    COIN_POINTS     = 10

    def __init__(
        self,
        name: str,
        track_rect: pygame.Rect,
        car: Car,
        accent_color: tuple[int, int, int],
    ) -> None:
        self.name = name
        self.track_rect = track_rect.copy()
        self.car = car
        self.accent_color = accent_color

        self.alive = True
        self.survival_time = 0.0
        self.coins_collected = 0
        self.audio = None
        self.weapon = Weapon()
        self.projectiles = []

        self.obstacles: list[Obstacle] = []
        self.items: list[Consumable] = []

        self._obstacle_spawn_timer = 0.0
        self._item_spawn_timer = 3.0
        self._coin_spawn_timer = 0.8
        self._lane_offset = 0.0
        self._speed_boost_timer = 0.0
        self._oil_timer = 0.0

        self._obstacle_sprites: list[str] = [
            str(_SPRITES_DIR / "obstaculo.png"),
            str(_SPRITES_DIR / "obstaculo2.png"),
        ]
        self.obstacle_types = [
            {"sprite": path, "static": False} for path in self._obstacle_sprites
        ]

    def current_world_speed(self) -> float:
        return 220.0 + min(220.0, self.survival_time * 14.0)

    @property
    def score(self) -> int:
        return self.coins_collected * self.COIN_POINTS

    def update(self, dt: float, keys) -> None:
        self.car.update_animation(dt)
        if not self.alive:
            return

        self.survival_time += dt
        self._update_active_effects(dt)
        self._lane_offset += self.current_world_speed() * dt

        self.car.update(dt, keys)
        self.weapon.update(dt)
        if keys[self.car.controls['fire']]:
            projectile = self.weapon.fire(self.car)
            if projectile is not None:
                self.projectiles.append(projectile)
                if self.audio:
                    self.audio.play('shot')

        self._obstacle_spawn_timer -= dt
        if self._obstacle_spawn_timer <= 0.0:
            self._spawn_obstacle()
            self._reset_obstacle_timer()

        for obstacle in self.obstacles:
            obstacle.update(dt)
        self.obstacles = [o for o in self.obstacles if o.rect().right > self.track_rect.left - 60]

        self._item_spawn_timer -= dt
        if self._item_spawn_timer <= 0.0:
            self._spawn_item()
            self._item_spawn_timer = random.uniform(3.0, 6.0)

        self._coin_spawn_timer -= dt
        if self._coin_spawn_timer <= 0.0:
            self._spawn_coin()
            self._coin_spawn_timer = random.uniform(1.0, 1.8)

        for item in self.items:
            item.update(dt)
        self.items = [i for i in self.items if i.rect().right > self.track_rect.left - 60]

        self._update_projectiles(dt)
        self._resolve_collisions()

    def _update_projectiles(self, dt: float) -> None:
        for projectile in self.projectiles[:]:
            projectile.update(dt)
            targets = sorted(self.obstacles, key=lambda obstacle: obstacle.position.x)
            hit = next((obstacle for obstacle in targets if projectile.swept_rect().colliderect(obstacle.rect())), None)
            if hit is not None:
                self.obstacles.remove(hit)
                self.projectiles.remove(projectile)
                if self.audio:
                    self.audio.play('crash')
            elif projectile.position.x > self.track_rect.right:
                self.projectiles.remove(projectile)

    def _spawn_obstacle(self) -> None:
        x = float(self.track_rect.right + random.randint(0, 280))
        y = float(random.randint(
            self.track_rect.top + 8,
            self.track_rect.bottom - self.OBSTACLE_HEIGHT - 8,
        ))

        base_speed = self.current_world_speed()
        speed = max(180.0, min(600.0, random.uniform(base_speed * 0.7, base_speed * 1.4)))
        obstacle_type = random.choice(self.obstacle_types)
        sprite_path = obstacle_type["sprite"]
        if obstacle_type["static"]:
            speed = base_speed

        self.obstacles.append(Obstacle(
            x=x,
            y=y,
            max_width=self.OBSTACLE_WIDTH,
            max_height=self.OBSTACLE_HEIGHT,
            speed=speed,
            sprite_path=sprite_path,
            acceleration_x=0.0,
        ))
        
    def _reset_obstacle_timer(self) -> None:
        dynamic_delay = max(0.0, 0.55 - self.survival_time * 0.02)
        self._obstacle_spawn_timer = random.uniform(
            0.28 + dynamic_delay,
            0.90 + dynamic_delay,
        )

    def _spawn_item(self) -> None:
        x = float(self.track_rect.right + random.randint(0, 280))
        y = float(random.randint(
            self.track_rect.top + 8,
            self.track_rect.bottom - self.ITEM_HEIGHT - 8,
        ))

        speed = float(random.randint(180, 350))
        effect = random.choice(["speed", "shield", "oleo"])

        if effect == "shield":
            sprite_path = str(_SPRITES_DIR / "shield.png")
        elif effect == "oleo":
            sprite_path = str(_SPRITES_DIR / "oleo.png")
        else:
            sprite_path = str(_SPRITES_DIR / "speed.png")

        self.items.append(Consumable(
            x=x,
            y=y,
            max_width=self.ITEM_WIDTH,
            max_height=self.ITEM_HEIGHT,
            speed=speed,
            effect=effect,
            sprite_path=sprite_path,
        ))

    def _spawn_coin(self) -> None:
        self.items.append(Consumable(
            x=float(self.track_rect.right + 40),
            y=random.uniform(self.track_rect.top + 8, self.track_rect.bottom - self.COIN_SIZE - 8),
            max_width=self.COIN_SIZE,
            max_height=self.COIN_SIZE,
            speed=self.current_world_speed(),
            effect='coin',
            sprite_path=str(_SPRITES_DIR / 'coin.png'),
        ))

    def _resolve_collisions(self) -> None:
        if not self.alive:
            return
        hit_obstacle, consumed_items, collided_obstacle = CollisionManager.resolve_basic(
            self.car, self.obstacles, self.items
        )

        if hit_obstacle and collided_obstacle is not None:
            if self.audio:
                self.audio.play('crash')
            if self.car.has_shield:
                self.car.has_shield = False
                if collided_obstacle in self.obstacles:
                    self.obstacles.remove(collided_obstacle)
            else:
                self.car.damaged = True
                self.alive = False
                return

        for consumed in consumed_items:
            if self.audio:
                self.audio.play('pickup')
            self._apply_consumable_effect(consumed.effect)

    def _apply_consumable_effect(self, effect: str) -> None:
        if effect == 'coin':
            self.coins_collected += 1
        elif effect == "speed":
            self._speed_boost_timer = 3.5
        elif effect == "oleo":
            self._oil_timer = 3.5
        elif effect == "shield":
            self.car.has_shield = True
        elif effect == "stability":
            self.car.FRICTION = min(900.0, self.car.FRICTION + 80.0)
        self._refresh_speed()

    def _update_active_effects(self, dt: float) -> None:
        self._speed_boost_timer = max(0.0, self._speed_boost_timer - dt)
        self._oil_timer = max(0.0, self._oil_timer - dt)
        self._refresh_speed()

    def _refresh_speed(self) -> None:
        self.car.MAX_SPEED = Car.MAX_SPEED + (30.0 if self._speed_boost_timer else 0.0) - (100.0 if self._oil_timer else 0.0)

    def draw(self, screen: pygame.Surface, font, small_font) -> None:
        previous_clip = screen.get_clip()
        screen.set_clip(self.track_rect)
        self._draw_track_background(screen)
        self._draw_lane_stripes(screen)

        for item in self.items:
            item.draw(screen)

        for obstacle in self.obstacles:
            obstacle.draw(screen)

        self.car.draw(screen)
        self.weapon.draw(screen, self.car)
        for projectile in self.projectiles:
            projectile.draw(screen)
        self._draw_hud(screen, font, small_font)
        screen.set_clip(previous_clip)

    def _draw_track_background(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, (70, 70, 70), self.track_rect)
        pygame.draw.rect(screen, self.accent_color, self.track_rect, 3)

    def _draw_lane_stripes(self, screen: pygame.Surface) -> None:
        stripe_w = 40
        gap = 30
        stripe_y = self.track_rect.centery - 4
        offset = int(self._lane_offset % (stripe_w + gap))
        x = self.track_rect.left - offset

        while x < self.track_rect.right:
            pygame.draw.rect(
                screen,
                (220, 220, 220),
                (x, stripe_y, stripe_w, 8),
                border_radius=3,
            )
            x += stripe_w + gap

    def _draw_hud(self, screen: pygame.Surface, font, small_font) -> None:
        name_surf   = font.render(self.name, True, self.accent_color)
        score_surf = small_font.render(f"Moedas: {self.coins_collected} | Pontos: {self.score}", True, (255, 220, 90))

        status_color = (120, 255, 120) if self.alive else (255, 120, 120)
        status_surf = small_font.render(
            "VIVO" if self.alive else "ELIMINADO", True, status_color
        )

        hud_x = self.track_rect.left + 10
        screen.blit(name_surf,   (hud_x, self.track_rect.top + 8))
        screen.blit(score_surf,  (hud_x, self.track_rect.top + 42))
        screen.blit(status_surf, (hud_x, self.track_rect.top + 64))


class PlayerLane(GameWorld):
    pass
