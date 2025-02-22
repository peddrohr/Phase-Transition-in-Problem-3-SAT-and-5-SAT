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
    tempo = solver.time()

    return isSatisfazivel, tempo

def transicao_fase(alpha_max: float, k: int, variaveis: list[int], instancias: int):
    resultados = []
    alpha_inicial = 0.0

    while alpha_inicial <= alpha_max:

        for n in variaveis:
            m = alpha_inicial * n
            satisfaziveis = 0
            tempo_total = 0.0

            for i in range(instancias):
                clausulas = gerar_clausulas(n, m, k)
                isSatisfazivel, tempo = solver_clausulas(clausulas)

                tempo_total += tempo

                if isSatisfazivel:
                    satisfaziveis += 1
                
            probabilidade = satisfaziveis / instancias
            media_tempo = tempo_total / instancias

            resultados.append({
                "n": n,
                "alpha": round(alpha_inicial, 1),
                "propabilidade": probabilidade,
                "tempo": media_tempo
            })
            print(f"variavel {n}")

        alpha_inicial = round(alpha_inicial + 0.1, 1)
        print(f"Alpha {alpha_inicial}")
    return resultados

def gerar_grafico(resultados: list[dict]):
    # Dicionário para organizar os dados por valor de n
    dados_por_n = {}

    # Organiza os resultados por valor de n
    for resultado in resultados:
        n = resultado["n"]
        alpha = resultado["alpha"]
        probabilidade = resultado["propabilidade"]
        tempo = resultado["tempo"]

        if n not in dados_por_n:
            dados_por_n[n] = {"alphas": [], "probabilidades": [], "tempos": []}

        dados_por_n[n]["alphas"].append(alpha)
        dados_por_n[n]["probabilidades"].append(probabilidade)
        dados_por_n[n]["tempos"].append(tempo)

    # Gráfico 1: Probabilidade de satisfazibilidade em função de alpha
    plt.figure(figsize=(10, 6))
    for n, dados in dados_por_n.items():
        plt.plot(dados["alphas"], dados["probabilidades"], label=f"n = {n}")
    
    plt.title("Probabilidade de Satisfazibilidade em Função de Alpha")
    plt.xlabel("Alpha α = m/n")
    plt.ylabel("Probabilidade de Satisfazibilidade")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"grafico_probabilidade.png")
    plt.close()

    # Gráfico 2: Tempo médio de execução em função de alpha
    plt.figure(figsize=(10, 6))
    for n, dados in dados_por_n.items():
        plt.plot(dados["alphas"], dados["tempos"], label=f"n = {n}")
    
    plt.title("Tempo Médio de Execução em Função de Alpha")
    plt.xlabel("Alpha (m/n)")
    plt.ylabel("Tempo Médio (segundos)")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"grafico_tempo.png")
    plt.close()

k_SAT = [3, 5]
n = [50, 100, 150, 200]
n_teste = [30] #variaveis y
instancias = 30

resultados = transicao_fase(20, 3, n, instancias)
gerar_grafico(resultados)



