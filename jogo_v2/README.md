# Race Tech — variação 1

Jogo local de corrida e sobrevivência para dois jogadores em Python/Pygame.

## Executar

Na raiz do repositório:

```powershell
python -m pip install -r requirements.txt
python jogo_v2/main.py
```

Requer Python 3.10 ou superior. Versão verificada: Python 3.12 e Pygame 2.6.1.

## Controles

- Jogador 1: WASD para mover; Espaço para disparar.
- Jogador 2: setas para mover; Ctrl direito para disparar.
- ESC: menu. No resultado: ENTER volta ao menu; R reinicia.
- Informe os nomes antes da partida. ENTER avança, TAB troca o campo.

Pontuação: 10 por segundo, 25 por coleta benéfica, 50 por obstáculo destruído. Óleo reduz a velocidade por 3,5 segundos; turbo aumenta pelo mesmo período; escudo absorve uma colisão. A arma dispara a cada 0,4 segundo enquanto a tecla estiver pressionada.

O histórico fica em `jogo_v2/data/scores.json`, fora do Git. Partidas abandonadas não são salvas. O menu Pontuações mostra o ranking completo em páginas.

## Organização

- `game/core/app.py`: aplicação e navegação entre telas.
- `game/core/scores.py`: leitura e gravação do histórico.
- `game/core/audio.py`: efeitos sonoros sintetizados.
- `game/phases/phase_1.py`: partida, resultado e música.
- `game/domain/gameWorld.py`: pista, objetos, efeitos e pontuação.
- `game/domain/entities.py`: vetores e hierarquia de objetos.
- `game/domain/animation.py`: sequências e conjuntos de animações.
- `game/domain/weapons.py`: arma e projéteis.
- `game/domain/collision.py`: colisões do carro.
- `game/interface/`: menu, seleção de fase, nomes, histórico e créditos.

## Testes

Na raiz, após instalar as dependências:

```powershell
$env:PYTHONPATH='jogo_v2'
python -m unittest discover -s jogo_v2/tests -v
```

Os testes usam tela e áudio simulados.
