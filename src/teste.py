import random
from pysat.solvers import Glucose4

def gerarClausula(n, m, k):
    clausulas = []

    while len(clausulas) < m:
        literal = sorted(random.sample(range(1, n+1), k))
        clausula = []
        for valor in literal:
            if random.random() > 0.5:
                clausula.append(valor)
            else:
                clausula.append(valor * -1)
        if clausula not in clausulas:
             clausulas.append(clausula)


    return clausulas



def solver(clausulas):
    solver = Glucose4(use_timer=True)
    for clausula in clausulas:
        solver.add_clause(clausula)
    
    satisfazivel = solver.solve()
    tempo = solver.time()

    return satisfazivel, tempo


ksat = [3, 5]
variaveis = [50, 100, 150]
instancias = 10

for x in ksat:
    alpha_inicio = 1.0
    alpha_fim = 10.0 if x == 3 else 20.0
    alpha_passos = 0.1
    
    num_points = int((alpha_fim - alpha_inicio) / alpha_passos) + 1
    alphas = [alpha_inicio + i * alpha_passos 
              for i in range(num_points)]
    
    for y in variaveis:
        print(f"Processing k={x}, n={y}")

        for alpha in alphas:
            m = int(alpha * y)
            if m < x:
                m = x

            quant_satisfazivel = 0
            tempo_total = 0.0




            for z in range(instancias):
                clausula = gerarClausula(y, m, x)
                satisfazivel, tempo = solver(clausula)
                if satisfazivel:
                    quant_satisfazivel += 1
                else:
                    quant_satisfazivel += 0
            tempo_total += tempo

            prob = quant_satisfazivel / instancias
            avg = tempo_total / instancias
            print(f"Alpha: {alpha:.2f}, Prob: {prob:.2f}, Time: {avg:.2f}s")
