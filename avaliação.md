# Avaliação - Desenvolvimento de um Jogo

**Curso:** Engenharia de Software  
**Componentes Curriculares:** Tópicos em Computação  
**Professores:** Eduardo Henrique Molina da Cruz

Durante o ano, os alunos deverão desenvolver um jogo.

- Poderá ser desenvolvido em equipes de até 3 pessoas.
- A proposta de trabalho da equipe deverá ser aprovada previamente pelo professor.

---

## Sobre a linguagem de programação

- A linguagem de programação deverá obrigatoriamente suportar orientação a objeto.
- Para poder atingir o conceito A, a linguagem de programação a ser usada deverá ser **C++**.
- Qualquer outra linguagem a ser usada limitará a equipe ao conceito B.

---

## Sobre o paradigma de programação

Deverá ser programado usando orientação a objeto, organizando adequadamente o código em classes (inclusive herança e polimorfismo quando apropriado).

> ⚠️ Quem não seguir estas restrições receberá o conceito **D**.

---

## Sobre bibliotecas e frameworks

Não poderá utilizar bibliotecas/frameworks/ferramentas que automatizam o processo de criação de jogos, tais como a Unity, Godot, dentre outras.

Os alunos estarão limitados a usar a biblioteca padrão da linguagem, bem como bibliotecas que facilitam o acesso a eventos de entrada (mouse, teclado, etc), manipulação multimídia (desenhar na tela, tocar áudio) e gerenciamento de física.

### Para equipes que usarem C++, fica pré-autorizado o uso das seguintes bibliotecas:

- Biblioteca padrão do C++;
- [Biblioteca my-lib](https://github.com/ehmcruz/my-lib), que possui várias utilidades de uso geral;
- [Biblioteca de manipulação de eventos e multimídia SDL2](https://www.libsdl.org/);
- Para carregar vários formatos de textura: **SDL Image**;
- Para imprimir texto: **SDL TTF**;
- Para manipular o áudio: **SDL Mixer**;
- Para desenhar geometrias variadas: **SDL GFX**;
- [Biblioteca de física Box2D](https://github.com/erincatto/box2d).

### Para equipes que usarem Python, fica pré-autorizado o uso das seguintes bibliotecas:

- PyGame;
- Biblioteca de física Box2D adaptada para Python.

> 💡 O professor adverte que, para jogos com física simples, é mais fácil implementar sua própria física do que usar o Box2D.

O uso de qualquer outra biblioteca ou framework necessita de aprovação prévia pelo professor.

> ⚠️ Quem não seguir estas restrições receberá o conceito **D**.

---

## Sobre o uso de ferramentas de inteligência artificial

Fica autorizado o uso de inteligência artificial para:

- Aprender sobre a linguagem e bibliotecas;
- Gerar os assets multimídia do jogo, como sprites e áudio;
- Uso de ferramentas de auto-completar códigos, como GitHub Copilot;
- Uso de agentes de inteligência artificial, como GitHub Copilot, para auxiliar na escrita de funções de forma isolada.

A inteligência artificial deverá ser usada apenas como **ferramenta de apoio**. O comando e tomada de decisões deve estar com a equipe.

> ⚠️ Se usarem IA para auxiliar na escrita do código, mas não souberem explicar o que a IA fez, terão problemas. Quem infringir as regras de uso de inteligência artificial receberá o conceito **D**.

---

## Sobre as entregas periódicas, questionamentos e validações

- Os alunos deverão obrigatoriamente armazenar o código em **repositório público no GitHub**.
- Deverão ser feitos commits regularmente, com ao menos **1 commit semanal**. Commits "falsos" ou com poucas alterações serão desconsiderados. O não cumprimento da frequência mínima de commits acarretará desconto no conceito.
- Os alunos serão questionados regularmente sobre o código escrito, que deverá ser validado com o professor. Alunos que não souberem responder adequadamente aos questionamentos não terão o código validado, acarretando desconto no conceito, podendo até mesmo ser atribuído conceito D.

---

## Sobre a dificuldade do jogo

O professor irá analisar a proposta de cada equipe para determinar o grau de dificuldade. Propostas consideradas de nível de dificuldade **baixa** terão redução de conceito no momento das avaliações.

---

## Demais observações

- Integrantes da equipe que não contribuírem adequadamente no desenvolvimento do projeto terão seus conceitos reduzidos, podendo chegar ao conceito D.
- Integrantes da equipe que não usarem o tempo em sala de aula adequadamente para o desenvolvimento do projeto terão seus conceitos reduzidos, podendo chegar ao conceito D.
- Equipes disfuncionais, no qual o professor perceba que algum membro não contribui adequadamente, poderão ser dissolvidas pelo professor, tendo seus membros que continuar o trabalho individualmente.
- Lembrem-se: **o código funcionar não significa que está bom.**

---

## Arquitetura, organização e estrutura do código

Por se tratar de um primeiro jogo, será usada a forma mais simples: arquitetura baseada em orientação a objetos.

A ideia é estabelecer um conjunto comum de parâmetros a todos os objetos e criar um motor que processe esses parâmetros. Por exemplo, em um jogo de plataforma, poderia ser comum a todos os objetos:

- Posição;
- Velocidade;
- Massa;
- Força;
- Hitbox, hurtbox e collider.

### Principais classes recomendadas

#### `GameManager`
Classe responsável por fazer a inicialização das bibliotecas, menus, GameWorld, e é responsável também por fazer o main loop do jogo. No main loop, os eventos são capturados e redirecionados para o GameWorld ativo, e é também feito o controle dos FPS e redirecionamento da execução para o GameWorld.

Com um desenvolvimento mais avançado, a GameManager é responsável por manter o estado do jogo (se está em um menu, ou no mundo do jogo, etc).

#### `GameWorld`
É a classe que representa o mundo do jogo. Ela contém os objetos, gerencia a física, colisões, e todos os aspectos do jogo. A cada frame, chama as funções de todos seus objetos (`GameObject`) ativos.

Alguns jogos podem possuir mais de um GameWorld (ex: um RPG de turnos com um GameWorld para o mapa e outro para as batalhas). O GameWorld pode ser derivado de uma classe abstrata `GameScene`, e nesse caso a GameManager se comunicaria apenas com a GameScene.

#### `GameObject`
Classe abstrata que contém um objeto genérico, com funções virtuais (polimórficas) para renderização, processamento de física, atualização do objeto, processamento de eventos, etc.

Exemplo de hierarquia a partir de `GameObject`:

```
GameObject
├── StaticObject     (objetos estáticos do cenário)
└── DynamicObject    (objetos dinâmicos)
    └── Character    (coisas comuns a todos os personagens)
        ├── Player
        └── Enemy
```

> Esta hierarquia é apenas um exemplo comum. É responsabilidade de cada equipe estruturar uma organização adequada das classes de seu jogo.

---

## Recomendações gerais

- Desenvolver uma hierarquia entre as classes dos objetos, do mais genérico ao mais especializado.
- Escrever um código bem organizado, modular e limpo. Fazer reaproveitamento de código.
- Não ficar micro-gerenciando cada objeto individualmente. Escrever um motor que processa objetos de forma automatizada a partir dos parâmetros do objeto.
- Processar a física usando as equações reais, cuidando das unidades:
  ```
  posição += velocidade;          // ❌ errado
  posição += velocidade * tempo;  // ✅ correto
  ```
  *(tempo = tempo de processamento do frame anterior)*
- Para unidades geométricas como ponto e vetores (posição, velocidade), não trabalhar com variáveis independentes para os eixos x e y. Criar uma estrutura que agrupe x e y em um único objeto.
  - Em C++: a biblioteca `my-lib` possui `math-vector.h`.
  - Com Box2D: o mesmo já possui uma biblioteca de vetores.
- Vetores e pontos, apesar de serem distintos, podem compartilhar a mesma estrutura.
- Não usar números inteiros para armazenar posição/velocidade. Usar **ponto flutuante**.
- Idealmente, não trabalhar usando pixel como unidade de posição — usar uma unidade adequada à lógica do jogo e converter para pixel somente na renderização *(não obrigatório, mas recomendado)*.

---

## Configurando o ambiente C++

- **Linux:** usar o ecossistema nativo do GCC.
- **Windows:** usar o ambiente MSYS2, conforme tutorial:
  [Tutorial MSYS2](https://docs.google.com/document/d/12-BqAJ0QttZrezhZ2U-1WBjn9nJwic4n3X5_e_lNNSw/edit?usp=sharing)
  - Instalar todos os pacotes necessários da SDL2 (UCRT64).
- Para incluir a My-lib no projeto, seguir o tutorial:
  [Tutorial My-lib](https://docs.google.com/document/d/1-7h4SxHaPt4VoR2UzizN6hxWBoRDskQ8dLciieBbjQw/edit?usp=sharing)

---

## Cronograma de desenvolvimento do projeto

### Trimestre 1
- Usar alguma estrutura de dados (STL em C++).
- Ter a física/mecânica implementada adequadamente.
- Conter toda a estrutura das classes.
- Estar "jogável", mesmo que algumas features estejam faltando.
- A representação dos objetos pode ser feita temporariamente por figuras geométricas.
- Ter preparado os sprites, efeitos sonoros e música de fundo (para inserir no Trimestre 2).

### Trimestre 2
- Ter áudio, efeitos sonoros, música de fundo.
- Ter os sprites e animações respectivas.
- Ter todas as features que se espera do jogo proposto.
- Ter algum sistema de pontos.

### Trimestre 3
- Ter um menu que permita iniciar o jogo, sair, etc.
- Após concluído o jogo, exibir tela de encerramento e voltar ao menu.
- Item no menu para mostrar o histórico de pontuação dos jogadores (salvar o nome do jogador no score).
- Item no menu com os créditos.
- Acabamentos finais do jogo.
- Publicar resumo na SETIF.
- Apresentar na IFTECH.
- Apresentar na Mostra de Curso.

---

## Descrição das avaliações

### Trimestre 1

| Avaliação | Descrição | Data |
|-----------|-----------|------|
| Avaliação 1 | Avaliação focada no código-fonte (programação) | 15/04/2026 |
| Avaliação 2 | Avaliação focada nos aspectos artísticos | 15/04/2026 |
| Recuperação paralela – Avaliação 1 | Nova oportunidade de entrega da Avaliação 1 | 06/05/2026 |
| Recuperação paralela – Avaliação 2 | Nova oportunidade de entrega da Avaliação 2 | 06/05/2026 |

### Trimestre 2

| Avaliação | Descrição | Data |
|-----------|-----------|------|
| Avaliação 1 | Avaliação focada no código-fonte (programação) | — |
| Avaliação 2 | Avaliação focada nos aspectos artísticos | — |
| Recuperação paralela – Avaliação 1 | Nova oportunidade de entrega da Avaliação 1 | — |
| Recuperação paralela – Avaliação 2 | Nova oportunidade de entrega da Avaliação 2 | — |

### Trimestre 3

| Avaliação | Descrição | Data |
|-----------|-----------|------|
| Avaliação 1 | Avaliação focada no código-fonte (programação) | — |
| Avaliação 2 | Avaliação focada nos aspectos artísticos | — |
| Recuperação paralela – Avaliação 1 | Nova oportunidade de entrega da Avaliação 1 | — |
| Recuperação paralela – Avaliação 2 | Nova oportunidade de entrega da Avaliação 2 | — |

---

## Critérios avaliativos

### Código-fonte
- Linguagem de programação utilizada;
- Dificuldade de implementação;
- Qualidade do código escrito;
- Boas práticas de programação;
- Completude;
- Corretude;
- Experiência do usuário;
- Respostas aos questionamentos do professor;
- Entregas periódicas.

### Arte do projeto
- Qualidade da arte;
- Completude;
- Coerência;
- Experiência do usuário;
- Respostas aos questionamentos do professor;
- Entregas periódicas.

---

## Atribuição de conceitos

| Conceito | Descrição |
|----------|-----------|
| **A** | Aprendizagem **plena**, atingindo todos os objetivos |
| **B** | Aprendizagem **parcialmente plena**, atingindo os objetivos |
| **C** | Aprendizagem **suficiente**, atingindo os objetivos |
| **D** | Aprendizagem **insuficiente**, não atingindo os objetivos |

### Tabela para cálculo do conceito final de cada trimestre

|  | **Avaliação 2: A** | **Avaliação 2: B** | **Avaliação 2: C** | **Avaliação 2: D** |
|--|--|--|--|--|
| **Avaliação 1: A** | A | B | C | D |
| **Avaliação 1: B** | B | B | C | D |
| **Avaliação 1: C** | C | C | C | D |
| **Avaliação 1: D** | D | D | D | D |