import random
from pysat.formula import CNF
from pysat.solvers import Glucose3
import time

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
    ns = [50, 100, 150, 200]
    num_instances = 30  # Reduced for testing
    results = {}

    for k in ks:
        alpha_start = 1.0
        alpha_end = 10.0 if k == 3 else 20.0
        alpha_step = 0.5  # Larger step for testing
        alphas = [alpha_start + i * alpha_step for i in range(int((alpha_end - alpha_start) / alpha_step) + 1)]
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
                print(f"Alpha: {alpha:.1f}, Prob: {prob:.2f}, Time: {avg_time:.2f}s")

    # Print results
    for k in ks:
        print(f"\nResults for {k}-SAT:")
        for n in ns:
            print(f"  n={n}:")
            for alpha, prob, avg_time in zip(results[k][n]['alphas'], results[k][n]['probs'], results[k][n]['times']):
                print(f"    Alpha: {alpha:.1f}, Prob: {prob:.2f}, Time: {avg_time:.2f}s")

if __name__ == "__main__":
    main()