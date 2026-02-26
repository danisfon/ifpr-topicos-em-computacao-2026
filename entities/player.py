import pygame
from setting import SCREEN_WIDTH, SCREEN_HEIGHT


class Player:
    def __init__(self, x, y, size, speed, controls, color):
        self.x = x
        self.y = y
        self.base_size = size #tamanho oringial
        self.size = size #tamanho atual
        self.w = size #largura atual
        self.h = size #altura atual

        self.speed = speed
        self.controls = controls  # dicionário de teclas
        self.color = color

        # dano
        self.health = 100
        self.hit_cooldown = 0 

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

#Coloca limite na tela (evita que o jogador saia da janela)
        if self.x < 0:
            self.x = 0
        if self.x + self.size > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.size
        if self.y < 0:
            self.y = 0
        if self.y + self.size > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.size

    def take_hit(self, amount=10):
        """Aplica dano e 'amassa' o carro (deforma o retângulo)."""
        if self.hit_cooldown > 0:
            return

        self.health = max(0, self.health - amount)

        # Deformação simples: achata e reduz levemente
        # (simulando amassado)
        self.w = max(18, self.w - 6)      # reduz largura até um mínimo
        self.h = max(18, self.h - 4)      # reduz altura até um mínimo

        self.hit_cooldown = 15  # ~0.5s se FPS=30

    def update(self):
        """Atualizações por frame (cooldown, etc)."""
        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1


    def draw(self, screen):
        rect = self.get_rect()

        # desenha o corpo
        pygame.draw.rect(screen, self.color, rect, border_radius=6)

        # desenha “rachaduras”/linhas pretas conforme vida baixa (efeito simples)
        if self.health <= 70:
            pygame.draw.line(screen, (0,0,0), rect.topleft, rect.bottomright, 2)
        if self.health <= 40:
            pygame.draw.line(screen, (0,0,0), rect.topright, rect.bottomleft, 2)

        # barrazinha de vida em cima do carro
        bar_w = rect.width
        bar_h = 6
        pct = self.health / 100
        pygame.draw.rect(screen, (60,60,60), (rect.x, rect.y - 10, bar_w, bar_h))
        pygame.draw.rect(screen, (0,255,0), (rect.x, rect.y - 10, int(bar_w * pct), bar_h))
