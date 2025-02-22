from pysat.solvers import Glucose4
import matplotlib.pyplot as plt
import random



def gerar_clausulas(n: int, m: int, k: int):
    clausulas = []

    while len(clausulas) < m:
        literais = sorted(random.sample(range(1, n+1), k))
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
    tempo = solver.time()*1000

    return isSatisfazivel, tempo

def encontrar_ponto_critico(alphas, probabilidades):
    for i in range(len(probabilidades)):
        if probabilidades[i] < 0.5:
            return alphas[i]
    return None

def transicao_fase(alpha_max: float, k: int, variaveis: list[int], instancias: int):
    resultados = {n: {"alphas": [], "probabilidades": [], "tempos": []} for n in variaveis}

    alpha_inicial = 1.0
    print(f'k:{k}')
    while alpha_inicial <= alpha_max:
        print(f'alpha:{alpha_inicial}')
        for n in variaveis:
            m = alpha_inicial * n
            satisfaziveis = 0
            tempo_total = 0.0

            print(f'variaveis:{n}')
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

    for n, dados in resultados.items():
        ponto_critico = encontrar_ponto_critico(dados["alphas"], dados["probabilidades"])

        gerar_grafico(
            dados["alphas"], dados["probabilidades"], n,
            f"Probabilidade de Satisfazibilidade Pelo Alpha {k}-SAT de {n} variaveis ",
            "Alpha = m/n", "Probabilidade", f"probabilidade {n} {k}-SAT de {n} variaveis ", ponto_critico
        )

        gerar_grafico(
            dados["alphas"], dados["tempos"], n,
            f"Tempo Médio de Resolução {k}-SAT de {n} variaveis",
            "Alpha = m/n", "Tempo (milisegundos)", f"tempo {n} {k}-SAT de {n} variaveis", ponto_critico
        )


def gerar_grafico(x, y, n, title, xlabel, ylabel, name_img, ponto_critico=None):
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, label=f"n = {n}")

    if ponto_critico is not None:

        y_critico = None
        for i in range(len(x)):
            if x[i] >= ponto_critico:
                y_critico = y[i]
                break

        if y_critico is not None:
            plt.scatter(ponto_critico, y_critico, color='red', zorder=5, label=f'Interseção (α = {ponto_critico}, y = {y_critico:.2f})')

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.legend()
    plt.savefig(f"{name_img}.png")
    plt.close()

n = [[50, 100, 150, 200],[20, 30, 40, 50]]
instancias = 30
alpha = [10,30]
k_sat = [3,5]


transicao_fase(alpha[0], k_sat[0], n[0], instancias)
transicao_fase(alpha[1], k_sat[1], n[1], instancias)