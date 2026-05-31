# Mission Control AI

Sistema em **Python** que simula o monitoramento inteligente de uma missão espacial experimental. A partir de dados simulados, o programa acompanha a missão ciclo a ciclo, gera alertas automáticos, calcula o nível de risco, identifica a tendência da operação e a área mais afetada, e entrega um **relatório final completo no terminal**.

Projeto desenvolvido para a **Global Solution**.

- **Missão:** Orion Test Alpha
- **Equipe:** Equipe Apollo

---

## Sobre o projeto

A indústria espacial depende de sistemas capazes de acompanhar o funcionamento de missões, satélites e módulos experimentais. Durante uma missão, informações como temperatura, comunicação, bateria, oxigênio e estabilidade precisam ser analisadas continuamente. A partir desses dados, um sistema computacional pode identificar riscos, emitir alertas e sugerir ações para apoiar a tomada de decisão.

O **Mission Control AI** é a primeira versão de um sistema com esse objetivo. A missão é simulada por meio de **ciclos de monitoramento**, em que cada ciclo representa um momento da operação. A cada ciclo o sistema responde automaticamente: a missão está estável, em atenção ou crítica? Qual área apresenta maior risco? A situação está melhorando ou piorando? Qual recomendação deve ser apresentada?

---

## O que foi desenvolvido

- **Base de dados da missão** organizada em uma matriz (`dados_missao`) com 6 ciclos, cada um com 5 informações monitoradas.
- **Classificação automática** de cada informação em `NORMAL`, `ATENÇÃO` ou `CRÍTICO`, com mensagem explicativa.
- **Cálculo do nível de risco** de cada ciclo (de 0 a 10 pontos) e **classificação do ciclo** em MISSÃO ESTÁVEL, EM ATENÇÃO ou CRÍTICA.
- **Recomendações automáticas** em cada ciclo, que priorizam as situações mais graves (vários sistemas críticos acionam o modo de segurança).
- **Análise de tendência**, comparando o risco do primeiro com o do último ciclo (melhora, piora ou estável).
- **Identificação da área mais afetada**, somando o risco de cada área ao longo de toda a missão.
- **Relatório final** com médias, ciclo mais crítico, risco médio, quantidade de ciclos críticos, tendência, pontuação por área, classificação final e conclusão.
- Código organizado em **19 funções**, com laço de repetição para percorrer os ciclos e estruturas condicionais para gerar os alertas.

---

## Como executar

É necessário ter o **Python 3** instalado (testado na versão 3.12).

```bash
python mission_control_ai.py
```

ou, em alguns sistemas:

```bash
python3 mission_control_ai.py
```

> Em consoles antigos do Windows, se os acentos não aparecerem, rode `chcp 65001` antes de executar (o programa já tenta forçar a codificação UTF-8 automaticamente).

Para usar os dados da sua própria equipe, altere `NOME_MISSAO`, `NOME_EQUIPE` e os valores da matriz `dados_missao`, no topo do arquivo.

---

## Como funciona

### Estrutura dos dados

A base do projeto é a matriz `dados_missao` (uma lista de listas). Cada **linha** é um ciclo de monitoramento; cada **coluna** é uma informação, sempre nesta ordem:

```python
dados_missao = [
    [23, 97, 89, 99, 94],   # Ciclo 1 - operação nominal
    [26, 80, 73, 95, 85],   # Ciclo 2 - sistemas estabilizados
    [29, 28, 61, 92, 76],   # Ciclo 3 - blecaute parcial de comunicação
    [36, 47, 44, 87, 60],   # Ciclo 4 - superaquecimento e desgaste geral
    [39, 25, 17, 81, 34],   # Ciclo 5 - falha múltipla, pico da crise
    [31, 56, 39, 86, 52],   # Ciclo 6 - tentativa de recuperação
]
```

| Posição | Informação   | Unidade | Área correspondente        |
|:-------:|--------------|:-------:|----------------------------|
| 0       | Temperatura  | °C      | Temperatura interna        |
| 1       | Comunicação  | %       | Comunicação com a base     |
| 2       | Bateria      | %       | Sistema de energia         |
| 3       | Oxigênio     | %       | Suporte de oxigênio        |
| 4       | Estabilidade | %       | Estabilidade operacional   |

A lista `areas_monitoradas` está relacionada, na mesma ordem, às colunas da matriz e é usada no relatório final.

### Regras de classificação dos alertas

Cada informação é classificada conforme as faixas abaixo:

**Temperatura (°C)** — menor que 18: ATENÇÃO · de 18 a 30: NORMAL · de 30 a 35: ATENÇÃO · acima de 35: CRÍTICO

**Comunicação (%)** — menor que 30: CRÍTICO · de 30 a 59: ATENÇÃO · 60 ou mais: NORMAL

**Bateria (%)** — menor que 20: CRÍTICO · de 20 a 49: ATENÇÃO · 50 ou mais: NORMAL

**Oxigênio (%)** — menor que 80: CRÍTICO · de 80 a 89: ATENÇÃO · 90 ou mais: NORMAL

**Estabilidade (%)** — menor que 40: CRÍTICO · de 40 a 69: ATENÇÃO · 70 ou mais: NORMAL

### Pontuação e classificação do ciclo

Cada classificação gera uma pontuação de risco: **NORMAL = 0**, **ATENÇÃO = 1**, **CRÍTICO = 2**. Como cada ciclo tem 5 informações, a pontuação máxima é **10 pontos**.

| Pontuação total | Classificação        |
|:---------------:|----------------------|
| 0 a 2           | MISSÃO ESTÁVEL       |
| 3 a 5           | MISSÃO EM ATENÇÃO    |
| 6 a 10          | MISSÃO CRÍTICA       |

### Análises automáticas

- **Tendência:** compara o risco do primeiro ciclo com o do último (piora, melhora ou estável).
- **Área mais afetada:** soma o risco de cada área ao longo de todos os ciclos; a de maior pontuação é a mais afetada.
- **Classificação final:** aplica a tabela acima ao risco médio de todos os ciclos.

---

## Exemplo de saída

Execução com os dados de exemplo do projeto:

```
============================================================
RELATÓRIO FINAL DA MISSÃO
============================================================
Missão: Orion Test Alpha
Equipe: Equipe Apollo
Quantidade de ciclos analisados: 6

Média de temperatura: 30.67 °C
Média de comunicação: 55.50%
Média de bateria: 53.83%
Média de oxigênio: 90.00%
Média de estabilidade: 66.83%

Ciclo mais crítico: Ciclo 5
Maior pontuação de risco: 9
Risco médio da missão: 3.67
Quantidade de ciclos críticos: 2

Tendência da missão:
A missão apresentou tendência de piora.

Pontuação acumulada por área:
Temperatura interna: 5 pontos
Comunicação com a base: 6 pontos
Sistema de energia: 4 pontos
Suporte de oxigênio: 3 pontos
Estabilidade operacional: 4 pontos

Área mais afetada:
Comunicação com a base

Classificação final da missão:
MISSÃO EM ATENÇÃO
```

<details>
<summary>Ver saída completa (todos os ciclos)</summary>

```
============================================================
MISSION CONTROL AI
============================================================
Missão: Orion Test Alpha
Equipe: Equipe Apollo
Quantidade de ciclos analisados: 6
============================================================

CICLO 1
------------------------------------------------------------
Temperatura: 23 °C | NORMAL | Temperatura estável
Comunicação: 97% | NORMAL | Comunicação estável
Bateria: 89% | NORMAL | Energia estável
Oxigênio: 99% | NORMAL | Oxigênio adequado
Estabilidade: 94% | NORMAL | Estabilidade operacional adequada
Pontuação de risco do ciclo: 0
Classificação do ciclo: MISSÃO ESTÁVEL
Recomendação: Manter operação normal e continuar monitoramento.

CICLO 2
------------------------------------------------------------
Temperatura: 26 °C | NORMAL | Temperatura estável
Comunicação: 80% | NORMAL | Comunicação estável
Bateria: 73% | NORMAL | Energia estável
Oxigênio: 95% | NORMAL | Oxigênio adequado
Estabilidade: 85% | NORMAL | Estabilidade operacional adequada
Pontuação de risco do ciclo: 0
Classificação do ciclo: MISSÃO ESTÁVEL
Recomendação: Manter operação normal e continuar monitoramento.

CICLO 3
------------------------------------------------------------
Temperatura: 29 °C | NORMAL | Temperatura estável
Comunicação: 28% | CRÍTICO | Comunicação com a base em nível crítico
Bateria: 61% | NORMAL | Energia estável
Oxigênio: 92% | NORMAL | Oxigênio adequado
Estabilidade: 76% | NORMAL | Estabilidade operacional adequada
Pontuação de risco do ciclo: 2
Classificação do ciclo: MISSÃO ESTÁVEL
Recomendação: Tentar restabelecer contato com a base.

CICLO 4
------------------------------------------------------------
Temperatura: 36 °C | CRÍTICO | Risco de superaquecimento
Comunicação: 47% | ATENÇÃO | Comunicação instável
Bateria: 44% | ATENÇÃO | Bateria abaixo do recomendado
Oxigênio: 87% | ATENÇÃO | Oxigênio abaixo do ideal
Estabilidade: 60% | ATENÇÃO | Estabilidade operacional reduzida
Pontuação de risco do ciclo: 6
Classificação do ciclo: MISSÃO CRÍTICA
Recomendação: Verificar controle térmico da missão.

CICLO 5
------------------------------------------------------------
Temperatura: 39 °C | CRÍTICO | Risco de superaquecimento
Comunicação: 25% | CRÍTICO | Comunicação com a base em nível crítico
Bateria: 17% | CRÍTICO | Bateria em nível crítico
Oxigênio: 81% | ATENÇÃO | Oxigênio abaixo do ideal
Estabilidade: 34% | CRÍTICO | Estabilidade operacional crítica
Pontuação de risco do ciclo: 9
Classificação do ciclo: MISSÃO CRÍTICA
Recomendação: Ativar modo de segurança e priorizar suporte à vida, energia e comunicação.

CICLO 6
------------------------------------------------------------
Temperatura: 31 °C | ATENÇÃO | Temperatura elevada
Comunicação: 56% | ATENÇÃO | Comunicação instável
Bateria: 39% | ATENÇÃO | Bateria abaixo do recomendado
Oxigênio: 86% | ATENÇÃO | Oxigênio abaixo do ideal
Estabilidade: 52% | ATENÇÃO | Estabilidade operacional reduzida
Pontuação de risco do ciclo: 5
Classificação do ciclo: MISSÃO EM ATENÇÃO
Recomendação: Monitorar sistemas em atenção e preparar plano de contingência.
```

</details>

---

## Estrutura do código

O projeto atende ao requisito de **pelo menos 5 funções** (são 19 no total):

| Função | Responsabilidade |
|--------|------------------|
| `analisar_temperatura`, `analisar_comunicacao`, `analisar_bateria`, `analisar_oxigenio`, `analisar_estabilidade` | Classificam cada informação e devolvem `(classificação, mensagem)` |
| `analisar_ciclo` | Analisa as 5 informações de um ciclo |
| `calcular_pontuacao_ciclo` | Soma os pontos de risco do ciclo |
| `classificar_ciclo` | Classifica o ciclo (ou a missão) pela pontuação |
| `gerar_recomendacao` | Gera a recomendação automática do ciclo |
| `analisar_tendencia` | Compara o primeiro e o último ciclo |
| `acumular_pontos_por_area` | Soma o risco de cada área ao longo da missão |
| `identificar_area_mais_afetada` | Encontra a área com maior risco acumulado |
| `calcular_media_coluna` | Calcula a média de uma informação |
| `exibir_cabecalho`, `exibir_ciclo` | Exibem as informações no terminal |
| `gerar_conclusao` | Monta a conclusão da missão |
| `processar_missao` | Percorre todos os ciclos e consolida os dados |
| `gerar_relatorio_final` | Exibe o relatório final |
| `main` | Função principal do programa |

---

## Requisitos atendidos

- [x] Nome da missão e da equipe
- [x] Matriz `dados_missao` com 6 ciclos, cada um com 5 informações na ordem correta
- [x] Lista de áreas monitoradas
- [x] Mais de 5 funções
- [x] Estrutura de repetição para percorrer os ciclos
- [x] Estruturas condicionais para gerar os alertas
- [x] Cálculo de risco por ciclo e classificação de cada ciclo
- [x] Análise da tendência da missão
- [x] Identificação da área mais afetada
- [x] Relatório final exibido no terminal

---

## Equipe

| Integrante | RM |
|------------|----|
| *(preencher)* | *(preencher)* |

Mission Control AI — Global Solution.
