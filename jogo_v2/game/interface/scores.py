import pygame
from pathlib import Path
from .leaderboard import LeaderboardScreen


class ScoreScreens:
    def __init__(self, screen, clock, font, store):
        self.screen, self.clock, self.font, self.store = screen, clock, font, store
        self.title_font = pygame.font.SysFont('Arial', 46, bold=True)
        self.label_font = pygame.font.SysFont('Arial', 26, bold=True)
        self.hint_font = pygame.font.SysFont('Arial', 18)
        self.car_preview = None

    def name_layout(self):
        width, height = self.screen.get_size()
        card_width = min(480, (width - 120) // 2)
        left = (width - card_width * 2 - 24) // 2
        top = height // 2 - 120
        cards = [pygame.Rect(left + i * (card_width + 24), top, card_width, 270) for i in range(2)]
        fields = [pygame.Rect(card.x + 24, card.y + 132, card.width - 48, 58) for card in cards]
        button = pygame.Rect(width // 2 - 160, top + 310, 320, 54)
        return cards, fields, button

    def draw_names(self, names, selected, errors, message='', ready=False):
        width, height = self.screen.get_size()
        self.screen.fill((12, 14, 19))
        for x in range(-height, width, 90):
            pygame.draw.line(self.screen, (19, 22, 29), (x, height), (x + height, 0), 2)
        pygame.draw.rect(self.screen, (222, 43, 60), (0, 0, width, 6))

        def text(value, font, color, position, centered=False):
            surface = font.render(value, True, color)
            rect = surface.get_rect(midtop=position) if centered else surface.get_rect(topleft=position)
            self.screen.blit(surface, rect)

        text('RACE TECH / PREPARAÇÃO', self.hint_font, (235, 80, 92), (width // 2, 58), True)
        text('Quem vai para a pista?', self.title_font, (245, 246, 250), (width // 2, 88), True)
        text('Cadastre dois pilotos com nomes únicos para começar.', self.font, (155, 164, 181), (width // 2, 151), True)
        cards, fields, button = self.name_layout()
        if self.car_preview is None:
            path = Path(__file__).resolve().parents[2] / 'assets' / 'sprites' / 'playerBranco.png'
            image = pygame.image.load(str(path)).convert_alpha()
            image = image.subsurface(image.get_bounding_rect())
            self.car_preview = pygame.transform.smoothscale(image, (108, max(1, round(image.get_height() * 108 / image.get_width()))))
        for i, (card, field) in enumerate(zip(cards, fields)):
            accent = (241, 76, 92) if i == 0 else (70, 191, 232)
            pygame.draw.rect(self.screen, (24, 28, 37), card, border_radius=16)
            pygame.draw.rect(self.screen, accent if selected == i else (49, 56, 70), card, 2, border_radius=16)
            pygame.draw.rect(self.screen, accent, (card.x + 24, card.y + 26, 6, 28), border_radius=3)
            text(f'PILOTO 0{i + 1}', self.label_font, (240, 243, 248), (card.x + 44, card.y + 24))
            self.screen.blit(self.car_preview, (card.right - 135, card.y + 26))
            text('W A S D  /  ESPAÇO: disparar' if i == 0 else 'SETAS  /  CTRL DIR.: disparar', self.hint_font, (157, 167, 187), (card.x + 24, card.y + 78))
            text('NOME DO PILOTO', self.hint_font, (157, 167, 187), (field.x, field.y - 25))
            pygame.draw.rect(self.screen, (13, 17, 24), field, border_radius=8)
            pygame.draw.rect(self.screen, (255, 105, 112) if errors[i] else accent if selected == i else (55, 64, 80), field, 2, border_radius=8)
            color = (245, 246, 250) if names[i] else (108, 120, 142)
            old_clip = self.screen.get_clip()
            self.screen.set_clip(field.inflate(-24, -8))
            text(names[i] or 'Digite um nome', self.label_font, color, (field.x + 14, field.y + 14))
            if selected == i and pygame.time.get_ticks() % 1000 < 550:
                cursor_x = field.x + 15 + self.label_font.size(names[i])[0]
                pygame.draw.line(self.screen, accent, (cursor_x, field.y + 15), (cursor_x, field.bottom - 14), 2)
            self.screen.set_clip(old_clip)
            text(errors[i] or 'Até 18 caracteres • nome exclusivo', self.hint_font, (255, 130, 138) if errors[i] else (128, 140, 161), (field.x, field.bottom + 12))
        pygame.draw.rect(self.screen, (211, 39, 59) if ready else (53, 59, 73), button, border_radius=10)
        text('IR PARA A PISTA  →', self.label_font, (255, 255, 255) if ready else (155, 165, 182), (button.centerx, button.y + 12), True)
        text(message or 'Os nomes ficam reservados após confirmar o cadastro.', self.hint_font, (255, 130, 138) if message else (140, 151, 171), (width // 2, button.bottom + 14), True)
        text('TAB: trocar piloto     ENTER: continuar     ESC: voltar', self.hint_font, (157, 167, 187), (width // 2, height - 42), True)
        pygame.display.flip()

    def names(self):
        names = ['', '']
        selected = 0
        errors = ['', '']
        message = ''
        try:
            registered = self.store.registered_names()
        except (OSError, ValueError):
            registered = None
            message = 'Não foi possível ler os cadastros. Volte ao menu e tente novamente.'
        pygame.key.start_text_input()
        try:
            while True:
                self.clock.tick(60)
                for event in pygame.event.get():
                    submit = False
                    if event.type == pygame.QUIT:
                        return 'exit'
                    if event.type == pygame.TEXTINPUT:
                        names[selected] = (names[selected] + ''.join(c for c in event.text if c.isprintable()))[:18]
                        errors[selected] = ''
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        _, fields, button = self.name_layout()
                        for i, field in enumerate(fields):
                            if field.collidepoint(event.pos):
                                selected = i
                        submit = button.collidepoint(event.pos)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            return 'menu'
                        if event.key == pygame.K_BACKSPACE:
                            names[selected] = names[selected][:-1]
                            errors[selected] = ''
                        if event.key == pygame.K_TAB:
                            selected = 1 - selected
                        if event.key == pygame.K_RETURN:
                            if selected == 0:
                                errors = self.store.validate_names(names, registered or [])
                                if not errors[0]:
                                    selected = 1
                                    errors[1] = ''
                            else:
                                submit = True
                    if submit and registered is not None:
                        errors = self.store.validate_names(names, registered)
                        if any(errors):
                            selected = next(i for i, error in enumerate(errors) if error)
                        else:
                            try:
                                return self.store.register_names(names)
                            except (OSError, ValueError) as error:
                                message = f'Não foi possível cadastrar: {error}'
                ready = registered is not None and not any(self.store.validate_names(names, registered))
                self.draw_names(names, selected, errors, message, ready)
        finally:
            pygame.key.stop_text_input()

    def history(self):
        return LeaderboardScreen(self.screen, self.clock, self.store).run()
