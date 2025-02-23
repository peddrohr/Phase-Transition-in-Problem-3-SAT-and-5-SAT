from pysat.solvers import Glucose4
import matplotlib.pyplot as plt
import random

def gerar_clausulas(n, m, k):
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

def solver_clausulas(clausulas):
    solver = Glucose4(use_timer=True)

    for clausula in clausulas:
        solver.add_clause(clausula)

    isSatisfazivel = solver.solve()
    tempo = solver.time() * 1000  # Convertendo para milissegundos

    return isSatisfazivel, tempo

def encontrar_ponto_critico(alphas, probabilidades):
    for i in range(len(probabilidades)):
        if probabilidades[i] < 0.5:
            return alphas[i]
    return None

def transicao_fase(alpha_max, k, variaveis, instancias):
    resultados = {n: {"alphas": [], "probabilidades": [], "tempos": []}
                  for n in variaveis}

    alpha_inicial = 1.0
    print(f'k: {k}')
    while alpha_inicial <= alpha_max:
        print(f'alpha: {alpha_inicial}')
        for n in variaveis:
            m = int(alpha_inicial * n)  # Garantindo que m seja inteiro
            satisfaziveis = 0
            tempo_total = 0.0

            print(f'variáveis: {n}')
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

    # Gerar gráficos separados para probabilidade e tempo
    gerar_grafico_probabilidade(resultados, k, "Probabilidade de Satisfazibilidade", "Alpha = m/n", "Probabilidade", f"probabilidade_{k}-SAT")
    gerar_grafico_tempo(resultados, k, "Tempo Médio de Resolução", "Alpha = m/n", "Tempo (milisegundos)", f"tempo_{k}-SAT")

def gerar_grafico_probabilidade(resultados, k, title, xlabel, ylabel, name_img):
    plt.figure(figsize=(10, 6))
    
    for n, dados in resultados.items():
        plt.plot(dados["alphas"], dados["probabilidades"], label=f"n = {n}")

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.legend()
    plt.savefig(f"{name_img}.png")
    plt.close()

def gerar_grafico_tempo(resultados, k, title, xlabel, ylabel, name_img):
    plt.figure(figsize=(10, 6))
    
    for n, dados in resultados.items():
        plt.plot(dados["alphas"], dados["tempos"], label=f"n = {n}")

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
