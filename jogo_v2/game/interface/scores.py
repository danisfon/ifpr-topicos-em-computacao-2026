import pygame


class ScoreScreens:
    def __init__(self, screen, clock, font, store):
        self.screen, self.clock, self.font, self.store = screen, clock, font, store

    def draw_lines(self, title, lines):
        self.screen.fill((18, 18, 22))
        for index, text in enumerate([title, '', *lines]):
            image = self.font.render(text, True, (240, 240, 240))
            self.screen.blit(image, (60, 35 + index * 36))
        pygame.display.flip()

    def names(self):
        names = ['', '']
        selected = 0
        pygame.key.start_text_input()
        try:
            while True:
                self.clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return 'exit'
                    if event.type == pygame.TEXTINPUT:
                        names[selected] = (names[selected] + ''.join(c for c in event.text if c.isprintable()))[:18]
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            return 'menu'
                        if event.key == pygame.K_BACKSPACE:
                            names[selected] = names[selected][:-1]
                        if event.key == pygame.K_TAB:
                            selected = 1 - selected
                        if event.key == pygame.K_RETURN:
                            if selected == 0:
                                selected = 1
                            else:
                                return tuple(name.strip() or f'Jogador {i + 1}' for i, name in enumerate(names))
                self.draw_lines('Nome dos jogadores', [
                    ('> ' if selected == i else '  ') + f'Jogador {i + 1}: {name}_'
                    for i, name in enumerate(names)
                ] + ['', 'Digite o nome | TAB: trocar | ENTER: continuar | ESC: menu'])
        finally:
            pygame.key.stop_text_input()

    def history(self):
        try:
            rows = self.store.read()
            error = None
        except (OSError, ValueError):
            rows, error = [], 'Não foi possível ler o histórico. O arquivo foi preservado.'
        page = 0
        while True:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'exit'
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                        return 'menu'
                    if event.key == pygame.K_RIGHT:
                        page = min(max(0, (len(rows) - 1) // 10), page + 1)
                    if event.key == pygame.K_LEFT:
                        page = max(0, page - 1)
            lines = [f"{page * 10 + i + 1}. {r['name']} — {r['score']} pontos — {r['date'][:10]}"
                     for i, r in enumerate(rows[page * 10:page * 10 + 10])]
            self.draw_lines('Histórico de pontuação', (lines or [error or 'Nenhuma partida concluída.']) + [
                '', f'Página {page + 1} | Setas: páginas | ENTER/ESC: menu'])
