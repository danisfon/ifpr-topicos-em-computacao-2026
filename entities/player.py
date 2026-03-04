import pygame
from setting import SCREEN_WIDTH, SCREEN_HEIGHT


class Player:
    def __init__(self, x, y, size, speed, controls, color):
        self.x = x
        self.y = y
        self.base_size = size
        self.size = size 
        self.w = size 
        self.h = size 
        self.speed = speed
        self.controls = controls  
        self.color = color


    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), int(self.w), int(self.h))

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[self.controls["left"]]:
            self.x -= self.speed
        if keys[self.controls["right"]]:
            self.x += self.speed
        if keys[self.controls["up"]]:
            self.y -= self.speed
        if keys[self.controls["down"]]:
            self.y += self.speed

        if self.x < 0:
            self.x = 0
        if self.x + self.size > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.size
        if self.y < 0:
            self.y = 0
        if self.y + self.size > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.size

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))