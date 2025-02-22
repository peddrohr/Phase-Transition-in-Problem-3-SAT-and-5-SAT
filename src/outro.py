from pysat.solvers import Glucose4
import matplotlib.pyplot as plt
import random


def gerar_clausulas(n: int, m: int, k: int):
    clausulas = []

    while len(clausulas) < m:
        literais = sorted(random.sample(range(1, n + 1), k))
        clausula = []

        for literal in literais:
            isPositive = random.choice([True, False])
            if isPositive:
                clausula.append(literal)
            else:
                clausula.append(-literal)

        if clausula not in clausulas:
            clausulas.append(clausula)

    return clausulas


def solver_clausulas(clausulas: list[int]):
    solver = Glucose4(use_timer=True)

    for clausula in clausulas:
        solver.add_clause(clausula)

    isSatisfazivel = solver.solve()
    tempo = solver.time()

    return isSatisfazivel, tempo


def transicao_fase(alpha_max: float, k: int, variaveis: list[int], instancias: int):
    resultados = {n: {"alphas": [], "probabilidades": [], "tempos": []}
                  for n in variaveis}

    alpha_inicial = 0.0

    while alpha_inicial <= alpha_max:
        for n in variaveis:
            m = int(alpha_inicial * n)
            satisfaziveis = 0
            tempo_total = 0.0

            for _ in range(instancias):
                clausulas = gerar_clausulas(n, m, k)
                isSatisfazivel, tempo = solver_clausulas(clausulas)

                tempo_total += tempo

                if isSatisfazivel:
                    satisfaziveis += 1

            resultados[n]["alphas"].append(round(alpha_inicial, 1))
            resultados[n]["probabilidades"].append(satisfaziveis / instancias)
            resultados[n]["tempos"].append(tempo_total / instancias)

        alpha_inicial = round(alpha_inicial + 0.1, 1)

    gerar_grafico(
        resultados,
        "alphas",
        "probabilidades",
        "Probabilidade de Satisfazibilidade Pelo Alpha",
        "Alpha = m/n",
        "Probabilidade",
        "probabilidade.png"
    )

    gerar_grafico(
        resultados,
        "alphas",
        "tempos",
        "Tempo Médio de Resolução",
        "Alpha = m/n",
        "Tempo (segundos)",
        "tempo.png"
    )


def gerar_grafico(resultados, x, y, title, xlabel, ylabel, name_img):
    plt.figure(figsize=(10, 6))

    for n, dados in resultados.items():
        plt.plot(dados[x], dados[y], label=f"n = {n}")

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.legend()
    plt.savefig(name_img)
    plt.close()


k_SAT = [3, 5]
n_teste = [10, 20, 30, 40, 50]  # teste
instancias = 30

resultados = transicao_fase(10, 5, n_teste, instancias)
