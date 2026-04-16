# Jogo 2 - Corrida Horizontal

## Estrutura (POO)

- `main.py`: ponto de entrada.
- `game/core/app.py`: orquestra menu, seleção de fase e execução das fases.
- `game/core/config.py`: configurações e controles.
- `game/domain/entities.py`: entidades (`Vec2`, `Car`, `Obstacle`).
- `game/domain/player_lane.py`: estado e lógica de cada jogador (independente).
- `game/ui/menu.py`: menu principal do `jogo_v2`.
- `game/ui/level_select.py`: seletor de fases do `jogo_v2`.
- `game/phases/phase_1.py`: implementação da fase 1.
- `assets/sounds/`: músicas da fase (arquivo `.mp3`).

## Organização de pastas

```
jogo_v2/
├── main.py
└── game/
	├── __init__.py
	├── core/
	│   ├── __init__.py
	│   ├── app.py
	│   └── config.py
	├── domain/
	│   ├── __init__.py
	│   ├── entities.py
	│   └── player_lane.py
	├── ui/
	│   ├── __init__.py
	│   ├── menu.py
	│   └── level_select.py
	├── phases/
	│   └── phase_1.py
└── assets/
	└── sounds/
```

## Requisitos atendidos

- Dois jogadores independentes.
- Corrida horizontal de sobrevivência.
- Obstáculos procedurais.
- Física de aceleração/atrito.
- Estrutura independente do jogo principal.
- Fase atual registrada como **Fase 1**.
