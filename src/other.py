import random
from pysat.formula import CNF
from pysat.solvers import Glucose3
import time
import matplotlib.pyplot as plt
import numpy as np


def generate_cnf(n, m, k):
    clauses = []
    clauses_set = set()
    max_attempts = 1000  # Prevent infinite loops

    while len(clauses) < m:
        variables = random.sample(range(1, n+1), k)
        clause = []
        for var in variables:
            if random.random() < 0.5:
                clause.append(var)
            else:
                clause.append(-var)
        clause_sorted = sorted(clause, key=lambda x: abs(x))
        clause_tuple = tuple(clause_sorted)
        if clause_tuple not in clauses_set:
            clauses_set.add(clause_tuple)
            clauses.append(clause)
        else:
            max_attempts -= 1
            if max_attempts == 0:
                break
    return clauses


def solve_instance(clauses):
    cnf = CNF()
    for clause in clauses:
        cnf.append(clause)
    solver = Glucose3()
    solver.append_formula(cnf.clauses)
    start_time = time.time()
    is_sat = solver.solve()
    end_time = time.time()
    solver.delete()
    return is_sat, end_time - start_time


def main():
    ks = [3, 5]
    ns = [50, 60]
    num_instances = 10  # Reduced for testing
    results = {}

    for k in ks:
        alpha_start = 1.0
        alpha_end = 10.0 if k == 3 else 20.0
        alpha_step = 0.5  # Larger step for testing
        alphas = np.arange(alpha_start, alpha_end + alpha_step, alpha_step)
        results[k] = {}

        for n in ns:
            results[k][n] = {'alphas': [], 'probs': [], 'times': []}
            print(f"Processing k={k}, n={n}")

            for alpha in alphas:
                m = int(alpha * n)
                if m < k:
                    m = k
                sat_count = 0
                total_time = 0.0

                for _ in range(num_instances):
                    clauses = generate_cnf(n, m, k)
                    is_sat, time_taken = solve_instance(clauses)
                    sat_count += 1 if is_sat else 0
                    total_time += time_taken

                prob = sat_count / num_instances
                avg_time = total_time / num_instances
                results[k][n]['alphas'].append(alpha)
                results[k][n]['probs'].append(prob)
                results[k][n]['times'].append(avg_time)
                print(
                    f"Alpha: {alpha:.1f}, Prob: {prob:.2f}, Time: {avg_time:.2f}s")

    # Plotting
    for k in ks:
        plt.figure(figsize=(10, 6))
        for n in ns:
            alphas = results[k][n]['alphas']
            probs = results[k][n]['probs']
            plt.plot(alphas, probs, marker='o', label=f'n={n}')
        plt.xlabel('Alpha (clauses/variables)')
        plt.ylabel('Probability of Satisfiability')
        plt.title(f'{k}-SAT Phase Transition')
        plt.legend()
        plt.grid(True)
        plt.savefig(f'{k}_sat_phase_transition.png')
        plt.close()

        plt.figure(figsize=(10, 6))
        for n in ns:
            alphas = results[k][n]['alphas']
            times = results[k][n]['times']
            plt.plot(alphas, times, marker='o', label=f'n={n}')
        plt.xlabel('Alpha (clauses/variables)')
        plt.ylabel('Average Solving Time (s)')
        plt.title(f'{k}-SAT Solving Time')
        plt.legend()
        plt.grid(True)
        plt.savefig(f'{k}_sat_solving_time.png')
        plt.close()


if __name__ == "__main__":
    main()
