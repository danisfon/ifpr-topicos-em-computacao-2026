# Jogo 2 - Corrida Horizontal

## Estrutura (POO)

- `main.py`: ponto de entrada.
- `game/config.py`: configurações e controles.
- `game/entities.py`: entidades (`Vec2`, `Car`, `Obstacle`).
- `game/player_lane.py`: estado e lógica de cada jogador (independente).
- `game/phases/phase_1.py`: implementação da fase 1.
- `game/app.py`: orquestra menu, seleção de fase e execução das fases.

## Requisitos atendidos

- Dois jogadores independentes.
- Corrida horizontal de sobrevivência.
- Obstáculos procedurais.
- Física de aceleração/atrito.
- Reaproveitamento de menu e seleção de fases do jogo principal.
- Fase atual registrada como **Fase 1**.
