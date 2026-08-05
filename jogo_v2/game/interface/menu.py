import pygame


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()

        self.title_font = pygame.font.SysFont("Arial", 72, bold=True)
        self.subtitle_font = pygame.font.SysFont("Arial", 26, bold=True)
        self.option_font = pygame.font.SysFont("Arial", 38, bold=True)
        self.footer_font = pygame.font.SysFont("Arial", 20)

        self.options = ["Iniciar", "Configuracoes", "Creditos", "Sair"]
        self.selected = 0

        self.bg_color = (10, 10, 10)
        self.red = (220, 0, 0)
        self.red_light = (255, 50, 50)
        self.white = (245, 245, 245)
        self.gray = (150, 150, 150)
        self.yellow = (255, 220, 0)
        self.green = (0, 255, 0)

    def draw_vertical_gradient(self, top_color, bottom_color):
        width = self.screen.get_width()
        height = self.screen.get_height()

        for y in range(height):
            ratio = y / height
            r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
            g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
            b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (width, y))

    def draw_checkered_strip(self, width, height):
        strip_height = 40
        square_size = 20
        y = height - strip_height

        for x in range(0, width, square_size):
            for row in range(2):
                color = self.white if (x // square_size + row) % 2 == 0 else (20, 20, 20)
                pygame.draw.rect(
                    self.screen,
                    color,
                    (x, y + row * (strip_height // 2), square_size, strip_height // 2)
                )

    def draw_side_bars(self, width, height):
        pygame.draw.rect(self.screen, self.red, (0, 0, 18, height))
        pygame.draw.rect(self.screen, self.red, (width - 18, 0, 18, height))

        pygame.draw.rect(self.screen, self.red_light, (25, 0, 5, height))
        pygame.draw.rect(self.screen, self.red_light, (width - 30, 0, 5, height))

    def draw_top_banner(self, width):
        banner_rect = pygame.Rect(0, 0, width, 120)
        pygame.draw.rect(self.screen, (25, 25, 25), banner_rect)
        pygame.draw.line(self.screen, self.red, (0, 115), (width, 115), 5)

        title_surface = self.title_font.render("RACE TECH", True, self.white)
        title_rect = title_surface.get_rect(center=(width // 2, 45))
        self.screen.blit(title_surface, title_rect)

    def draw_decorations(self, width):
        line_width = 320
        gap = 140
        y1 = 170
        y2 = 185

        center_x = width // 2

        pygame.draw.line(self.screen, self.red, (center_x - gap - line_width, y1), (center_x - gap, y1), 4)
        pygame.draw.line(self.screen, self.red, (center_x + gap, y1), (center_x + gap + line_width, y1), 4)

        pygame.draw.line(self.screen, self.gray, (center_x - gap - line_width + 30, y2), (center_x - gap - 30, y2), 2)
        pygame.draw.line(self.screen, self.gray, (center_x + gap + 30, y2), (center_x + gap + line_width - 30, y2), 2)

    def draw_options(self, width, height):
        panel_width = 500
        panel_height = 320
        panel_x = (width - panel_width) // 2
        panel_y = (height - panel_height) // 2

        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel.fill((15, 15, 15, 210))
        self.screen.blit(panel, (panel_x, panel_y))

        pygame.draw.rect(self.screen, self.red, (panel_x, panel_y, panel_width, panel_height), 3)

        start_y = panel_y + 45
        spacing = 62

        for i, option in enumerate(self.options):
            option_y = start_y + i * spacing
            is_selected = i == self.selected

            if is_selected:
                highlight_rect = pygame.Rect(panel_x + 25, option_y - 10, panel_width - 50, 46)
                pygame.draw.rect(self.screen, self.red, highlight_rect, border_radius=8)
                pygame.draw.rect(self.screen, self.white, highlight_rect, 2, border_radius=8)

                arrow_left = self.option_font.render(">", True, self.green)
                arrow_right = self.option_font.render("<", True, self.yellow)

                option_surface = self.option_font.render(option.upper(), True, self.white)
                option_rect = option_surface.get_rect(center=(width // 2, option_y + 12))

                self.screen.blit(arrow_left, (panel_x + 40, option_y - 2))
                self.screen.blit(option_surface, option_rect)
                self.screen.blit(arrow_right, (panel_x + panel_width - 65, option_y - 2))
            else:
                option_surface = self.option_font.render(option.upper(), True, self.gray)
                option_rect = option_surface.get_rect(center=(width // 2, option_y + 12))
                self.screen.blit(option_surface, option_rect)

    def draw_footer(self, width, height):
        tip_text = "Use ↑ e ↓ para navegar | ENTER para selecionar"
        footer_surface = self.footer_font.render(tip_text, True, self.white)
        footer_rect = footer_surface.get_rect(center=(width // 2, height - 70))
        self.screen.blit(footer_surface, footer_rect)

    def draw(self):
        width = self.screen.get_width()
        height = self.screen.get_height()

        self.draw_vertical_gradient((8, 8, 8), (30, 30, 30))
        self.draw_side_bars(width, height)
        self.draw_top_banner(width)
        self.draw_decorations(width)
        self.draw_options(width, height)
        self.draw_footer(width, height)
        self.draw_checkered_strip(width, height)

        pygame.display.flip()

    def run(self):
        running = True

        while running:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)

                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)

                    elif event.key == pygame.K_RETURN:
                        if self.selected == 0:
                            return "start"
                        if self.selected == 1:
                            return "settings"
                        if self.selected == 2:
                            return "credits"
                        if self.selected == 3:
                            return "exit"

            self.draw()
