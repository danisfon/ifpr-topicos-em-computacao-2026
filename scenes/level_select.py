import pygame


class LevelSelect:

    def __init__(self, screen):

        self.screen = screen
        self.clock = pygame.time.Clock()

        self.title_font = pygame.font.SysFont("Arial", 70, bold=True)
        self.font = pygame.font.SysFont("Arial", 24, bold=True)  # 🔥 NEGRITO

        self.white = (240, 240, 240)
        self.gray = (150, 150, 150)
        self.red = (220, 0, 0)
        self.dark = (30, 30, 30)

        self.cols = 5
        self.rows = 2

        self.selected = 0

        # fases
        self.levels = []
        for i in range(10):
            self.levels.append({
                "name": f"Nível {i+1}",
                "unlocked": True if i == 0 else False
            })

    def draw_background(self):

        width = self.screen.get_width()
        height = self.screen.get_height()

        for y in range(height):
            color = int(10 + (y / height) * 30)
            pygame.draw.line(self.screen, (color, color, color), (0, y), (width, y))

    def draw_grid(self):

        width = self.screen.get_width()
        height = self.screen.get_height()

        card_w = 200
        card_h = 140
        spacing_x = 40
        spacing_y = 40

        # largura total do grid
        total_width = self.cols * card_w + (self.cols - 1) * spacing_x
        start_x = (width - total_width) // 2

        # altura total do grid
        total_height = self.rows * card_h + (self.rows - 1) * spacing_y

        # centralização vertical ajustada
        start_y = (height - total_height) // 2 + 40

        for i, level in enumerate(self.levels):

            row = i // self.cols
            col = i % self.cols

            x = start_x + col * (card_w + spacing_x)
            y = start_y + row * (card_h + spacing_y)

            rect = pygame.Rect(x, y, card_w, card_h)

            # cor base
            if level["unlocked"]:
                color = self.dark
            else:
                color = (20, 20, 20)

            pygame.draw.rect(self.screen, color, rect, border_radius=8)

            # seleção
            if i == self.selected:
                pygame.draw.rect(self.screen, self.red, rect, 3, border_radius=8)

            # nome da fase (negrito)
            text = self.font.render(level["name"], True, self.white)
            text_rect = text.get_rect(center=(x + card_w // 2, y + 25))
            self.screen.blit(text, text_rect)

            # miniatura fake
            pygame.draw.rect(self.screen, (80, 80, 80),
                             (x + 10, y + 50, card_w - 20, 60))

            # cadeado
            if not level["unlocked"]:
                lock = self.font.render("🔒", True, self.gray)
                lock_rect = lock.get_rect(center=(x + card_w // 2, y + card_h // 2))
                self.screen.blit(lock, lock_rect)

    def draw(self):

        width = self.screen.get_width()

        self.draw_background()

        # título
        title = self.title_font.render("SELECIONE A FASE DESEJADA", True, self.white)
        rect = title.get_rect(center=(width // 2, 80))
        self.screen.blit(title, rect)

        self.draw_grid()

        pygame.display.flip()

    def run(self):

        while True:

            self.clock.tick(60)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    return "exit"

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        return "menu"

                    if event.key == pygame.K_RIGHT:
                        if (self.selected % self.cols) < self.cols - 1:
                            self.selected += 1

                    if event.key == pygame.K_LEFT:
                        if (self.selected % self.cols) > 0:
                            self.selected -= 1

                    if event.key == pygame.K_DOWN:
                        if self.selected + self.cols < len(self.levels):
                            self.selected += self.cols

                    if event.key == pygame.K_UP:
                        if self.selected - self.cols >= 0:
                            self.selected -= self.cols

                    if event.key == pygame.K_RETURN:
                        if self.levels[self.selected]["unlocked"]:
                            return self.selected

            self.draw()