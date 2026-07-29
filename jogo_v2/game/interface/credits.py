import pygame


class CreditsScreen:

    def __init__(self, screen):

        self.screen = screen
        self.clock = pygame.time.Clock()

        self.title_font = pygame.font.SysFont("Arial", 60, bold=True)
        self.subtitle_font = pygame.font.SysFont("Arial", 32, bold=True)
        self.text_font = pygame.font.SysFont("Arial", 26, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 20)

        self.white = (240, 240, 240)
        self.red = (220, 0, 0)
        self.gray = (180, 180, 180)
        self.yellow = (255,255,0)

    def draw_gradient(self):

        width = self.screen.get_width()
        height = self.screen.get_height()

        top_color = (10, 10, 10)
        bottom_color = (40, 40, 40)

        for y in range(height):

            ratio = y / height

            r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
            g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
            b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)

            pygame.draw.line(self.screen, (r, g, b), (0, y), (width, y))

    def draw_checkered_flag(self):

        width = self.screen.get_width()
        height = self.screen.get_height()

        size = 20
        start_y = height - 40

        for x in range(0, width, size):

            for row in range(2):

                if (x // size + row) % 2 == 0:
                    color = (255, 255, 255)
                else:
                    color = (30, 30, 30)

                pygame.draw.rect(
                    self.screen,
                    color,
                    (x, start_y + row * 20, size, 20)
                )

    def draw(self):

        width = self.screen.get_width()
        height = self.screen.get_height()

        self.draw_gradient()

        title = self.title_font.render("CRÉDITOS", True, self.white)
        title_rect = title.get_rect(center=(width // 2, 100))
        self.screen.blit(title, title_rect)

        pygame.draw.line(self.screen, self.red,
                         (width // 2 - 200, 140),
                         (width // 2 + 200, 140), 4)

        y = 220

        texts = [

            ("Desenvolvido por:", self.subtitle_font),

            ("Ali Chehade", self.text_font),
            ("Claudir Fantuci", self.text_font),
            ("Daniele Fonseca", self.text_font),

            ("", self.text_font),


            ("Professores:", self.subtitle_font),
            ("Eduardo Molina", self.text_font),
            ("Rafael Zottesso", self.text_font),
            ("Fabiano Utiyama", self.text_font),

             ("", self.text_font),

            ("Disciplina de Tópicos em Computação - IFPR Campus Paranavaí", self.text_font),
       
        ]
        
           

            
        for text, font in texts:

            if text == "Desenvolvido por:" or text == "Disciplina:" or text == "Professores:":
                color = self.yellow
            elif font == self.text_font:
                color = self.gray
            else:
                color = self.white

            surface = font.render(text, True, color)
            rect = surface.get_rect(center=(width // 2, y))

            self.screen.blit(surface, rect)

            y += 40

        tip = self.small_font.render(
            "Pressione ESC para voltar ao menu",
            True,
            self.white
        )

        tip_rect = tip.get_rect(center=(width // 2, height - 80))

        self.screen.blit(tip, tip_rect)

        self.draw_checkered_flag()

        pygame.display.flip()

    def run(self):

        running = True

        while running:

            self.clock.tick(60)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    return "exit"

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        return "menu"

            self.draw()