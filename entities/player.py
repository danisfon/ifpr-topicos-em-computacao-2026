import pygame
import math
from setting import SCREEN_WIDTH, SCREEN_HEIGHT


class Vec2:
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vec2(self.x * scalar, self.y * scalar)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalized(self):
        l = self.length()
        if l == 0:
            return Vec2(0.0, 0.0)
        return Vec2(self.x / l, self.y / l)

    def __repr__(self):
        return f"Vec2({self.x:.2f}, {self.y:.2f})"


class Player:
    ACCELERATION = 800.0   # pixels/s²
    FRICTION     = 600.0   # deceleration when no input (pixels/s²)
    MAX_SPEED    = 300.0   # pixels/s
    MASS         = 1.0     # kg (equal mass for both players)
    RESTITUTION  = 0.6     # bounciness coefficient (0 = no bounce, 1 = perfect elastic)

    def __init__(self, x, y, size, controls, color):
        self.position = Vec2(x, y)
        self.velocity = Vec2(0.0, 0.0)

        self.base_size = size
        self.size = float(size)
        self.w = float(size)
        self.h = float(size)

        self.controls = controls
        self.color = color

    def get_rect(self):
        return pygame.Rect(int(self.position.x), int(self.position.y),
                           int(self.w), int(self.h))

    def center(self):
        return Vec2(self.position.x + self.size / 2,
                    self.position.y + self.size / 2)

    def handle_input(self, delta_time: float):
        keys = pygame.key.get_pressed()

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

        if input_x != 0.0:
            self.velocity.x += input_x * self.ACCELERATION * delta_time
        else:
            if abs(self.velocity.x) > 0:
                friction_x = self.FRICTION * delta_time
                if abs(self.velocity.x) <= friction_x:
                    self.velocity.x = 0.0
                else:
                    self.velocity.x -= friction_x * (1 if self.velocity.x > 0 else -1)

        if input_y != 0.0:
            self.velocity.y += input_y * self.ACCELERATION * delta_time
        else:
            if abs(self.velocity.y) > 0:
                friction_y = self.FRICTION * delta_time
                if abs(self.velocity.y) <= friction_y:
                    self.velocity.y = 0.0
                else:
                    self.velocity.y -= friction_y * (1 if self.velocity.y > 0 else -1)

        self.velocity.x = max(-self.MAX_SPEED, min(self.MAX_SPEED, self.velocity.x))
        self.velocity.y = max(-self.MAX_SPEED, min(self.MAX_SPEED, self.velocity.y))

        self.position.x += self.velocity.x * delta_time
        self.position.y += self.velocity.y * delta_time

        if self.position.x < 0:
            self.position.x = 0.0
            self.velocity.x = 0.0
        if self.position.x + self.size > SCREEN_WIDTH:
            self.position.x = SCREEN_WIDTH - self.size
            self.velocity.x = 0.0
        if self.position.y < 0:
            self.position.y = 0.0
            self.velocity.y = 0.0
        if self.position.y + self.size > SCREEN_HEIGHT:
            self.position.y = SCREEN_HEIGHT - self.size
            self.velocity.y = 0.0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color,
                         (int(self.position.x), int(self.position.y),
                          int(self.size), int(self.size)))


def resolve_collision(a: Player, b: Player):
    overlap_x  = (a.position.x + a.size) - b.position.x
    overlap_x2 = (b.position.x + b.size) - a.position.x
    overlap_y  = (a.position.y + a.size) - b.position.y
    overlap_y2 = (b.position.y + b.size) - a.position.y

    if overlap_x <= 0 or overlap_x2 <= 0 or overlap_y <= 0 or overlap_y2 <= 0:
        return

    pen_x = min(overlap_x, overlap_x2)
    pen_y = min(overlap_y, overlap_y2)

    if pen_x < pen_y:
        normal    = Vec2(1.0, 0.0) if a.position.x < b.position.x else Vec2(-1.0, 0.0)
        separation = pen_x
    else:
        normal    = Vec2(0.0, 1.0) if a.position.y < b.position.y else Vec2(0.0, -1.0)
        separation = pen_y

    half = separation / 2.0
    a.position.x -= normal.x * half
    a.position.y -= normal.y * half
    b.position.x += normal.x * half
    b.position.y += normal.y * half

    rel_vel          = Vec2(a.velocity.x - b.velocity.x,
                            a.velocity.y - b.velocity.y)
    vel_along_normal = rel_vel.dot(normal)

    if vel_along_normal > 0:
        return

    e             = Player.RESTITUTION
    inv_mass_sum  = (1.0 / a.MASS) + (1.0 / b.MASS)
    j             = -(1.0 + e) * vel_along_normal / inv_mass_sum

    impulse_x = j * normal.x
    impulse_y = j * normal.y

    a.velocity.x += impulse_x / a.MASS
    a.velocity.y += impulse_y / a.MASS
    b.velocity.x -= impulse_x / b.MASS
    b.velocity.y -= impulse_y / b.MASS