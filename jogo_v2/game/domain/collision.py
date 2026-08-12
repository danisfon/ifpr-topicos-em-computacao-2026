from __future__ import annotations

from .entities import Car, Obstacle, Consumable


class CollisionManager:
    @staticmethod
    def resolve_basic(
        car: Car,
        obstacles: list[Obstacle],
        items: list[Consumable],
    ) -> tuple[bool, list[Consumable], Obstacle | None]:

        car_rect = car.rect()

        collided_obstacle: Obstacle | None = None
        for obstacle in obstacles:
            if car_rect.colliderect(obstacle.rect()):
                collided_obstacle = obstacle
                break

        consumed_items: list[Consumable] = []
        for item in items[:]:
            if car_rect.colliderect(item.rect()):
                items.remove(item)
                consumed_items.append(item)

        hit_obstacle = collided_obstacle is not None
        return hit_obstacle, consumed_items, collided_obstacle