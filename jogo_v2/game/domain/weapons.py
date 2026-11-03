from pathlib import Path
import pygame
from .entities import DynamicObject, Sprite, Vec2

SPRITES = Path(__file__).resolve().parents[2] / 'assets' / 'sprites'


class Projectile(DynamicObject):
    def __init__(self, position: Vec2):
        super().__init__(position.x, position.y, 28, 10, str(SPRITES / 'projectile.png'))
        self.velocity = Vec2(850.0, 0.0)
        self.previous_position = Vec2(position.x, position.y)

    def update(self, dt: float) -> None:
        self.previous_position = Vec2(self.position.x, self.position.y)
        self.update_motion(dt)

    def swept_rect(self) -> pygame.Rect:
        previous = self.rect().copy()
        previous.topleft = (round(self.previous_position.x), round(self.previous_position.y))
        return previous.union(self.rect())


class Weapon:
    COOLDOWN = 0.4

    def __init__(self):
        self.sprite = Sprite(str(SPRITES / 'weapon.png'), 42, 18)
        self.cooldown = 0.0

    def update(self, dt: float) -> None:
        self.cooldown = max(0.0, self.cooldown - dt)

    def fire(self, car) -> Projectile | None:
        if self.cooldown > 0.0:
            return None
        self.cooldown = self.COOLDOWN
        return Projectile(Vec2(car.position.x + car.size.x, car.position.y + car.size.y / 2.0 - 5.0))

    def draw(self, screen, car):
        screen.blit(self.sprite.surface, (car.position.x + car.size.x - self.sprite.width,
                                         car.position.y + car.size.y / 2.0 - self.sprite.height / 2.0))
