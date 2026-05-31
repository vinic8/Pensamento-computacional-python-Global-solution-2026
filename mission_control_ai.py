"""
Mission Control AI
==================
Sistema que simula o monitoramento inteligente de uma missão espacial
experimental.

O programa percorre os ciclos de monitoramento da missão, classifica cada
informação (NORMAL / ATENÇÃO / CRÍTICO), calcula o nível de risco de cada
ciclo, identifica a tendência da operação e a área mais afetada, e exibe um
relatório final no terminal.

Global Solution - primeira versão do Mission Control AI.
"""

import sys

# Garante que acentos e o símbolo de grau apareçam corretamente no terminal
# (inclusive em consoles do Windows). Se não for possível, segue normalmente.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


# ============================================================
# CONFIGURAÇÃO DA MISSÃO
# (troque pelo nome real da sua missão e da sua equipe)
# ============================================================

NOME_MISSAO = "Orion Test Alpha"
NOME_EQUIPE = "Equipe Apollo"

# Matriz principal da missão.
# Cada LINHA  = um ciclo de monitoramento.
# Cada COLUNA = uma informação, nesta ordem:
#   [temperatura, comunicacao, bateria, oxigenio, estabilidade]
dados_missao = [
    [23, 97, 89, 99, 94],   # Ciclo 1 - operação nominal, todos os sistemas estáveis
    [26, 80, 73, 95, 85],   # Ciclo 2 - sistemas estabilizados em rotina
    [29, 28, 61, 92, 76],   # Ciclo 3 - blecaute parcial de comunicação
    [36, 47, 44, 87, 60],   # Ciclo 4 - superaquecimento e desgaste geral
    [39, 25, 17, 81, 34],   # Ciclo 5 - falha múltipla, pico da crise
    [31, 56, 39, 86, 52],   # Ciclo 6 - tentativa de recuperação dos sistemas
]

# Áreas monitoradas (relacionadas, na mesma ordem, às colunas da matriz).
areas_monitoradas = [
    "Temperatura interna",        # coluna 0 -> temperatura
    "Comunicação com a base",     # coluna 1 -> comunicacao
    "Sistema de energia",         # coluna 2 -> bateria
    "Suporte de oxigênio",        # coluna 3 -> oxigenio
    "Estabilidade operacional",   # coluna 4 -> estabilidade
]

# Rótulos de classificação de cada informação e a pontuação de risco de cada um.
NORMAL = "NORMAL"
ATENCAO = "ATENÇÃO"
CRITICO = "CRÍTICO"

PONTOS = {
    NORMAL: 0,
    ATENCAO: 1,
    CRITICO: 2,
}

# Rótulos de classificação do ciclo (e da missão).
MISSAO_ESTAVEL = "MISSÃO ESTÁVEL"
MISSAO_ATENCAO = "MISSÃO EM ATENÇÃO"
MISSAO_CRITICA = "MISSÃO CRÍTICA"

# Linhas usadas na formatação do terminal.
LINHA_DUPLA = "=" * 60
LINHA_SIMPLES = "-" * 60


# ============================================================
# FUNÇÕES DE ANÁLISE DE CADA INFORMAÇÃO
# Cada função recebe o valor lido e devolve (classificacao, mensagem).
# ============================================================

def analisar_temperatura(temperatura):
    """Classifica a temperatura interna do módulo (em °C)."""
    if temperatura < 18:
        return ATENCAO, "Temperatura baixa"
    elif temperatura <= 30:
        return NORMAL, "Temperatura estável"
    elif temperatura <= 35:
        return ATENCAO, "Temperatura elevada"
    else:
        return CRITICO, "Risco de superaquecimento"


def analisar_comunicacao(comunicacao):
    """Classifica a qualidade do sinal de comunicação (em %)."""
    if comunicacao < 30:
        return CRITICO, "Comunicação com a base em nível crítico"
    elif comunicacao < 60:
        return ATENCAO, "Comunicação instável"
    else:
        return NORMAL, "Comunicação estável"


def analisar_bateria(bateria):
    """Classifica o nível de bateria da missão (em %)."""
    if bateria < 20:
        return CRITICO, "Bateria em nível crítico"
    elif bateria < 50:
        return ATENCAO, "Bateria abaixo do recomendado"
    else:
        return NORMAL, "Energia estável"


def analisar_oxigenio(oxigenio):
    """Classifica o nível de oxigênio disponível (em %)."""
    if oxigenio < 80:
        return CRITICO, "Oxigênio em nível crítico"
    elif oxigenio < 90:
        return ATENCAO, "Oxigênio abaixo do ideal"
    else:
        return NORMAL, "Oxigênio adequado"


def analisar_estabilidade(estabilidade):
    """Classifica a estabilidade geral dos sistemas (em %)."""
    if estabilidade < 40:
        return CRITICO, "Estabilidade operacional crítica"
    elif estabilidade < 70:
        return ATENCAO, "Estabilidade operacional reduzida"
    else:
        return NORMAL, "Estabilidade operacional adequada"


# Ordem das colunas: rótulo exibido, função de análise e unidade de medida.
ANALISADORES = [
    ("Temperatura", analisar_temperatura, " °C"),
    ("Comunicação", analisar_comunicacao, "%"),
    ("Bateria", analisar_bateria, "%"),
    ("Oxigênio", analisar_oxigenio, "%"),
    ("Estabilidade", analisar_estabilidade, "%"),
]


# ============================================================
# ANÁLISE DE UM CICLO
# ============================================================

def analisar_ciclo(ciclo):
    """
    Recebe uma linha da matriz (um ciclo) e devolve uma lista com a análise
    de cada uma das 5 informações monitoradas.

    Cada item é um dicionário:
        {"rotulo", "valor", "unidade", "classificacao", "mensagem", "pontos"}
    """
    analise = []
    for indice, (rotulo, funcao, unidade) in enumerate(ANALISADORES):
        valor = ciclo[indice]
        classificacao, mensagem = funcao(valor)
        analise.append({
            "rotulo": rotulo,
            "valor": valor,
            "unidade": unidade,
            "classificacao": classificacao,
            "mensagem": mensagem,
            "pontos": PONTOS[classificacao],
        })
    return analise


def calcular_pontuacao_ciclo(analise_ciclo):
    """Soma os pontos de risco das 5 informações do ciclo (0 a 10)."""
    pontuacao = 0
    for item in analise_ciclo:
        pontuacao += item["pontos"]
    return pontuacao


def classificar_ciclo(pontuacao):
    """
    Classifica o ciclo (ou a missão) a partir da pontuação de risco:
        0 a 2 -> MISSÃO ESTÁVEL
        3 a 5 -> MISSÃO EM ATENÇÃO
        6+    -> MISSÃO CRÍTICA
    """
    if pontuacao <= 2:
        return MISSAO_ESTAVEL
    elif pontuacao <= 5:
        return MISSAO_ATENCAO
    else:
        return MISSAO_CRITICA


# ============================================================
# RECOMENDAÇÕES AUTOMÁTICAS
# ============================================================

# Recomendação específica para cada área quando ela está em risco.
RECOMENDACAO_POR_AREA = {
    "Temperatura": "Verificar controle térmico da missão.",
    "Comunicação": "Tentar restabelecer contato com a base.",
    "Bateria": "Ativar modo de economia de energia.",
    "Oxigênio": "Acionar protocolo de suporte à vida.",
    "Estabilidade": "Reduzir operações não essenciais.",
}


def gerar_recomendacao(analise_ciclo):
    """
    Gera a recomendação do ciclo a partir da análise das 5 informações,
    priorizando as situações mais graves (CRÍTICO antes de ATENÇÃO).
    """
    criticos = [i for i in analise_ciclo if i["classificacao"] == CRITICO]
    atencoes = [i for i in analise_ciclo if i["classificacao"] == ATENCAO]

    # Tudo normal.
    if not criticos and not atencoes:
        return "Manter operação normal e continuar monitoramento."

    # Vários sistemas críticos ao mesmo tempo: modo de segurança.
    if len(criticos) >= 2:
        return ("Ativar modo de segurança e priorizar suporte à vida, "
                "energia e comunicação.")

    # Apenas um sistema crítico: recomendação específica daquele sistema.
    if len(criticos) == 1:
        return RECOMENDACAO_POR_AREA[criticos[0]["rotulo"]]

    # Sem críticos, apenas um sistema em atenção.
    if len(atencoes) == 1:
        return RECOMENDACAO_POR_AREA[atencoes[0]["rotulo"]]

    # Sem críticos, vários sistemas em atenção.
    return "Monitorar sistemas em atenção e preparar plano de contingência."


# ============================================================
# ANÁLISE DA TENDÊNCIA E DA ÁREA MAIS AFETADA
# ============================================================

def analisar_tendencia(risco_primeiro, risco_ultimo):
    """Compara o risco do primeiro ciclo com o do último ciclo."""
    if risco_ultimo > risco_primeiro:
        return "A missão apresentou tendência de piora."
    elif risco_ultimo < risco_primeiro:
        return "A missão apresentou tendência de melhora."
    else:
        return "A missão permaneceu estável em relação ao início."


def acumular_pontos_por_area(dados_missao):
    """
    Soma a pontuação de risco de cada área (coluna) ao longo de todos os
    ciclos. Devolve uma lista de 5 inteiros, na ordem de areas_monitoradas.
    """
    pontos_por_area = [0] * len(areas_monitoradas)
    for ciclo in dados_missao:
        analise = analisar_ciclo(ciclo)
        for indice, item in enumerate(analise):
            pontos_por_area[indice] += item["pontos"]
    return pontos_por_area


def identificar_area_mais_afetada(pontos_por_area):
    """Devolve o índice da área com maior pontuação de risco acumulada."""
    indice_maior = 0
    for indice in range(1, len(pontos_por_area)):
        if pontos_por_area[indice] > pontos_por_area[indice_maior]:
            indice_maior = indice
    return indice_maior


def calcular_media_coluna(dados_missao, coluna):
    """Calcula a média de uma coluna (uma informação) entre todos os ciclos."""
    total = 0
    for ciclo in dados_missao:
        total += ciclo[coluna]
    return total / len(dados_missao)


# ============================================================
# EXIBIÇÃO NO TERMINAL
# ============================================================

def exibir_cabecalho(quantidade_ciclos):
    """Imprime o cabeçalho do sistema."""
    print(LINHA_DUPLA)
    print("MISSION CONTROL AI")
    print(LINHA_DUPLA)
    print(f"Missão: {NOME_MISSAO}")
    print(f"Equipe: {NOME_EQUIPE}")
    print(f"Quantidade de ciclos analisados: {quantidade_ciclos}")
    print(LINHA_DUPLA)


def exibir_ciclo(numero, analise_ciclo, pontuacao, classificacao, recomendacao):
    """Imprime a análise completa de um ciclo."""
    print()
    print(f"CICLO {numero}")
    print(LINHA_SIMPLES)
    for item in analise_ciclo:
        rotulo = item["rotulo"]
        valor = item["valor"]
        unidade = item["unidade"]
        classif = item["classificacao"]
        mensagem = item["mensagem"]
        print(f"{rotulo}: {valor}{unidade} | {classif} | {mensagem}")
    print(f"Pontuação de risco do ciclo: {pontuacao}")
    print(f"Classificação do ciclo: {classificacao}")
    print(f"Recomendação: {recomendacao}")


def gerar_conclusao(classificacao_final):
    """Gera o texto de conclusão com base na classificação final da missão."""
    if classificacao_final == MISSAO_ESTAVEL:
        return ("A missão transcorreu de forma estável. Os sistemas "
                "permaneceram dentro dos parâmetros esperados e a operação "
                "pode seguir normalmente, mantendo o monitoramento de rotina.")
    elif classificacao_final == MISSAO_ATENCAO:
        return ("A missão apresentou instabilidade relevante durante a "
                "operação. Ainda existem sistemas em atenção e a equipe deve "
                "manter o plano de contingência ativo e o monitoramento "
                "reforçado.")
    else:
        return ("A missão atingiu condição crítica durante a operação. É "
                "necessário acionar os protocolos de emergência, priorizar o "
                "suporte à vida e reavaliar a continuidade da missão.")


# ============================================================
# PROCESSAMENTO E RELATÓRIO FINAL
# ============================================================

def processar_missao(dados_missao):
    """
    Percorre todos os ciclos, exibe a análise de cada um e devolve os dados
    consolidados usados no relatório final.
    """
    exibir_cabecalho(len(dados_missao))

    pontuacoes = []       # pontuação de risco de cada ciclo
    classificacoes = []   # classificação de cada ciclo

    # Estrutura de repetição que percorre todos os ciclos da missão.
    for numero, ciclo in enumerate(dados_missao, start=1):
        analise = analisar_ciclo(ciclo)
        pontuacao = calcular_pontuacao_ciclo(analise)
        classificacao = classificar_ciclo(pontuacao)
        recomendacao = gerar_recomendacao(analise)

        exibir_ciclo(numero, analise, pontuacao, classificacao, recomendacao)

        pontuacoes.append(pontuacao)
        classificacoes.append(classificacao)

    return pontuacoes, classificacoes


def gerar_relatorio_final(dados_missao, pontuacoes, classificacoes):
    """Exibe o relatório final consolidado da missão."""
    print()
    print(LINHA_DUPLA)
    print("RELATÓRIO FINAL DA MISSÃO")
    print(LINHA_DUPLA)
    print(f"Missão: {NOME_MISSAO}")
    print(f"Equipe: {NOME_EQUIPE}")
    print(f"Quantidade de ciclos analisados: {len(dados_missao)}")
    print()

    # Médias por informação monitorada.
    print(f"Média de temperatura: {calcular_media_coluna(dados_missao, 0):.2f} °C")
    print(f"Média de comunicação: {calcular_media_coluna(dados_missao, 1):.2f}%")
    print(f"Média de bateria: {calcular_media_coluna(dados_missao, 2):.2f}%")
    print(f"Média de oxigênio: {calcular_media_coluna(dados_missao, 3):.2f}%")
    print(f"Média de estabilidade: {calcular_media_coluna(dados_missao, 4):.2f}%")
    print()

    # Ciclo mais crítico, risco médio e quantidade de ciclos críticos.
    maior_risco = max(pontuacoes)
    ciclo_mais_critico = pontuacoes.index(maior_risco) + 1
    risco_medio = sum(pontuacoes) / len(pontuacoes)
    quantidade_criticos = classificacoes.count(MISSAO_CRITICA)

    print(f"Ciclo mais crítico: Ciclo {ciclo_mais_critico}")
    print(f"Maior pontuação de risco: {maior_risco}")
    print(f"Risco médio da missão: {risco_medio:.2f}")
    print(f"Quantidade de ciclos críticos: {quantidade_criticos}")
    print()

    # Tendência da missão (primeiro ciclo x último ciclo).
    tendencia = analisar_tendencia(pontuacoes[0], pontuacoes[-1])
    print("Tendência da missão:")
    print(tendencia)
    print()

    # Pontuação acumulada por área.
    pontos_por_area = acumular_pontos_por_area(dados_missao)
    print("Pontuação acumulada por área:")
    for indice, area in enumerate(areas_monitoradas):
        print(f"{area}: {pontos_por_area[indice]} pontos")
    print()

    # Área mais afetada.
    indice_area = identificar_area_mais_afetada(pontos_por_area)
    print("Área mais afetada:")
    print(areas_monitoradas[indice_area])
    print()

    # Classificação final da missão (com base no risco médio).
    classificacao_final = classificar_ciclo(risco_medio)
    print("Classificação final da missão:")
    print(classificacao_final)
    print()

    # Conclusão.
    print("Conclusão:")
    print(gerar_conclusao(classificacao_final))
    print(LINHA_DUPLA)


def main():
    """Função principal: roda a análise da missão e gera o relatório final."""
    pontuacoes, classificacoes = processar_missao(dados_missao)
    gerar_relatorio_final(dados_missao, pontuacoes, classificacoes)


if __name__ == "__main__":
    main()
