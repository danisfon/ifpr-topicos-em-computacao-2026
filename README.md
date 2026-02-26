# Race Tech

Para o projeto da disciplina de tópicos em computação, estamos desenvolvendo um jogo de corrida 2D visto de cima (top-down), onde dois jogadores competem na mesma pista.
Cada corrida ocorre sob diferentes condições climáticas que afetam diretamente a dirigibilidade e a aderência do veículo.

# Instalação:

```pip install pygame```

# Executar:
```python main.py```

# Sistema de Voltas

- Mesma linha de largada e chegada (linha com colisão invisível)
- Contador de voltas
- Tempo por volta

# Controles

Jogador 1:
- W -> Acelerar
- A -> Esquerda
- S -> Frear
- D -> Direita

Jogador 2:
- Setas direcionais

# Sistema de Colisão
A colisão será ativada contra:
- Paredes da pista (Designada pelas barreiras listradas)
- Outro jogador
