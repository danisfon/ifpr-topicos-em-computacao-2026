from datetime import datetime

import pygame


class LeaderboardScreen:
    PAGE_SIZE = 6
    WHITE = (241, 244, 250)
    MUTED = (151, 164, 185)
    MEDALS = ((255, 206, 90), (184, 204, 225), (221, 158, 113))

    def __init__(self, screen, clock, store):
        self.screen, self.clock, self.store = screen, clock, store
        self.title_font = pygame.font.SysFont('Arial', 42, bold=True)
        self.number_font = pygame.font.SysFont('Arial', 32, bold=True)
        self.row_font = pygame.font.SysFont('Arial', 22, bold=True)
        self.small_font = pygame.font.SysFont('Arial', 18)

    def layout(self):
        width, height = self.screen.get_size()
        content = pygame.Rect((width - min(1080, width - 80)) // 2, 0, min(1080, width - 80), height)
        back = pygame.Rect(content.x, height - 84, 220, 44)
        previous = pygame.Rect(content.right - 282, height - 84, 132, 44)
        following = pygame.Rect(content.right - 132, height - 84, 132, 44)
        return content, back, previous, following

    def text(self, value, font, color, position, align='topleft', max_width=None):
        value = str(value)
        if max_width is not None and font.size(value)[0] > max_width:
            while value and font.size(value + '…')[0] > max_width:
                value = value[:-1]
            value += '…'
        image = font.render(value, True, color)
        self.screen.blit(image, image.get_rect(**{align: position}))

    @staticmethod
    def date_label(value):
        try:
            return datetime.fromisoformat(value).strftime('%d/%m/%Y')
        except (ValueError, TypeError):
            return '—'

    def button(self, rect, label, enabled=True, primary=False):
        hovered = enabled and rect.collidepoint(pygame.mouse.get_pos())
        fill = (201, 39, 60) if primary else (38, 46, 61)
        if hovered:
            fill = (233, 57, 78) if primary else (57, 69, 89)
        if not enabled:
            fill = (22, 27, 36)
        pygame.draw.rect(self.screen, fill, rect, border_radius=9)
        self.text(label, self.small_font, self.WHITE if enabled else (81, 93, 112), rect.center, 'center')

    def draw(self, rows, page=0, error=None):
        width, height = self.screen.get_size()
        content, back, previous, following = self.layout()
        pages = max(1, (len(rows) + self.PAGE_SIZE - 1) // self.PAGE_SIZE)
        page = max(0, min(page, pages - 1))
        self.screen.fill((12, 14, 19))
        for x in range(-height, width, 90):
            pygame.draw.line(self.screen, (19, 22, 29), (x, height), (x + height, 0), 2)
        pygame.draw.rect(self.screen, (222, 43, 60), (0, 0, width, 6))
        self.text('RACE TECH / RESULTADOS', self.small_font, (235, 80, 92), (content.x, 32))
        self.text('Ranking da pista', self.title_font, self.WHITE, (content.x, 58))
        self.text('Cada corrida deixa sua marca.', self.small_font, self.MUTED, (content.x, 112))
        self.text(f'{len(rows)} resultados registrados', self.small_font, self.MUTED, (content.right, 82), 'topright')
        self.text('1 MOEDA = 10 PONTOS', self.small_font, self.MEDALS[0], (content.right, 112), 'topright')

        card_width = (content.width - 32) // 3
        for i in range(3):
            card = pygame.Rect(content.x + i * (card_width + 16), 157, card_width, 108)
            pygame.draw.rect(self.screen, (24, 28, 37), card, border_radius=12)
            pygame.draw.rect(self.screen, (53, 59, 73), card, 1, border_radius=12)
            accent = self.MEDALS[i]
            pygame.draw.circle(self.screen, accent, (card.x + 31, card.y + 32), 17)
            self.text(str(i + 1), self.row_font, (24, 28, 37), (card.x + 31, card.y + 32), 'center')
            row = rows[i] if i < len(rows) else None
            self.text(row['name'] if row else 'Posição disponível', self.row_font, self.WHITE if row else self.MUTED,
                      (card.x + 60, card.y + 18), max_width=card.width - 76)
            self.text(f"{row['score']:,}".replace(',', '.') if row else '—', self.number_font, accent, (card.x + 24, card.y + 57), max_width=card.width - 115)
            self.text('PONTOS', self.small_font, self.MUTED, (card.right - 20, card.y + 73), 'topright')

        table = pygame.Rect(content.x, 286, content.width, 316)
        pygame.draw.rect(self.screen, (20, 24, 33), table, border_radius=12)
        rank_x, name_x = table.x + 28, table.x + 113
        date_x, points_x = table.right - 240, table.right - 28
        for label, x in [('POS.', rank_x), ('PILOTO', name_x), ('DATA', date_x)]:
            self.text(label, self.small_font, self.MUTED, (x, table.y + 15))
        self.text('PONTOS', self.small_font, self.MUTED, (points_x, table.y + 15), 'topright')
        pygame.draw.line(self.screen, (47, 54, 69), (table.x + 20, table.y + 44), (table.right - 20, table.y + 44))

        for i, row in enumerate(rows[page * self.PAGE_SIZE:(page + 1) * self.PAGE_SIZE]):
            rank = page * self.PAGE_SIZE + i + 1
            y = table.y + 52 + i * 42
            if i % 2 == 0:
                pygame.draw.rect(self.screen, (27, 32, 43), (table.x + 10, y - 3, table.width - 20, 40), border_radius=5)
            accent = self.MEDALS[rank - 1] if rank <= 3 else self.MUTED
            self.text(f'{rank:02}', self.row_font, accent, (rank_x, y))
            self.text(row['name'], self.row_font, self.WHITE, (name_x, y), max_width=date_x - name_x - 25)
            self.text(self.date_label(row['date']), self.small_font, self.MUTED, (date_x, y + 3))
            self.text(f"{row['score']:,}".replace(',', '.'), self.row_font, self.MEDALS[0], (points_x, y), 'topright', max_width=105)

        if not rows:
            self.text('Histórico indisponível' if error else 'A pista espera seu primeiro recorde', self.row_font,
                      (255, 130, 138) if error else self.WHITE, (table.centerx, table.y + 125), 'midtop')
            self.text('Não foi possível ler os resultados. Seus dados foram preservados.' if error else 'Conclua uma corrida para aparecer aqui.',
                      self.small_font, self.MUTED, (table.centerx, table.y + 168), 'midtop')

        self.button(back, '←  VOLTAR AO MENU', primary=True)
        self.button(previous, '←  Anterior', page > 0)
        self.button(following, 'Próxima  →', page < pages - 1)
        self.text(f'Página {page + 1} de {pages}', self.small_font, self.WHITE, (content.centerx, back.centery), 'center')
        self.text('← →: páginas    •    ENTER / ESC: menu', self.small_font, self.MUTED, (content.centerx, height - 27), 'center')
        pygame.display.flip()

    def run(self):
        try:
            rows, error = self.store.read(), None
        except (OSError, ValueError):
            rows, error = [], True
        page = 0
        last_page = max(0, (len(rows) - 1) // self.PAGE_SIZE)
        while True:
            self.clock.tick(60)
            _, back, previous, following = self.layout()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'exit'
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                        return 'menu'
                    if event.key in (pygame.K_RIGHT, pygame.K_PAGEDOWN):
                        page += 1
                    if event.key in (pygame.K_LEFT, pygame.K_PAGEUP):
                        page -= 1
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back.collidepoint(event.pos):
                        return 'menu'
                    if previous.collidepoint(event.pos):
                        page -= 1
                    if following.collidepoint(event.pos):
                        page += 1
                if event.type == pygame.MOUSEWHEEL:
                    page -= event.y
                page = max(0, min(page, last_page))
            self.draw(rows, page, error)
