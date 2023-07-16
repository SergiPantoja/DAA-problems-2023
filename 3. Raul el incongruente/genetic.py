import numpy as np
import random

from brute_force import simultaneous_incongruence

def _generate_input(n):
    input = []
    for i in range(int(n)):
        ai = np.random.randint(1, 100)
        bi = np.random.randint(ai, 100)
        input.append((ai, bi))
    return input

def test(n):
    a = _generate_input(n)
    print(a, "\n")
    
    #x = simultaneous_incongruence(a)
    #print("using brute force algorithm:")
    #print("x = ", x)
    #if isinstance(x, int):
    #    for i in range(len(a)):
    #        if x % a[i][1] == a[i][0] % a[i][1]:
    #            print("x = " + str(x) + " is congruent with a[" + str(i) + "] = " + str(a[i][0]) + " mod b[" + str(i) + "] = " + str(a[i][1]) + "\n")

    print("\n\nusing genetic algorithm:")
    x = genetic_algorithm(1000, 200, a, 0.1)
    if x == -1:
        print("Solution not found")
    else:
        print("x = ", x)
        for i in range(len(a)):
            if x % a[i][1] == a[i][0] % a[i][1]:
                print("x = " + str(x) + " is congruent with a[" + str(i) + "] = " + str(a[i][0]) + " mod b[" + str(i) + "] = " + str(a[i][1]) + "\n")

def check_congruence(x, a, b):
    # return if x is congruent with a mod b
    return x % b == a % b

# genetic algorithm implementation
def _objective_f(x, congruences):
    # Our goal is to minimize the number of congruences satisfied by x
    # If an x is found that does not satisfy any congruences then it is
    # a valid solution.
    num_satisfied = 0
    for i in congruences:
        if check_congruence(x, i[0], i[1]):
            num_satisfied += 1
    return num_satisfied

def _generate_initial_pop(size):
    # Generate a population of size size
    print("Generating initial population\n")
    pop = []
    for i in range(size):
        pop.append(np.random.randint(0, 1000000))
    return pop

def _evaluate_pop(population, congruences):
    # evaluates the current population using the objective function
    scores = []
    for i in population:
        score = len(congruences) - _objective_f(i, congruences)
        scores.append(score)
    return scores

def _selection(population, scores):
    # selects one individual from the population. Higher score individuals
    # have greater chance of being selected.
    total_fitness = sum(scores)
    prob = [score / total_fitness for score in scores]
    cum_prob = [sum(prob[:i+1]) for i in range(len(prob))]
    r = random.random()
    for i, c_prob in enumerate(cum_prob):
        if r <= c_prob:
            return population[i]
        
def _crossover(parent1, parent2):
    # creates a new individual using p1 and p2
    if abs(parent1 - parent2) <= 2:
        return np.random.randint(1000000)
    child = random.randint(min(parent1, parent2) + 1, max(parent1, parent2) - 1)
    #print(f"child of {parent1} and {parent2}: {child}")
    return child

def _mutation(i, mutation_rate):
    r = random.random()
    return np.random.randint(1000000) if (r <= mutation_rate) else i


def genetic_algorithm(generations, pop_size, congruences, mutation_rate):
    pop = _generate_initial_pop(pop_size)
    print("initial", pop)
    for gen in range(generations):
        print("Generation: ", gen)
        scores = _evaluate_pop(pop, congruences)
        # check if an individual is a valid solution
        for i in range(len(scores)):
            if scores[i] == len(congruences):
                print("Solution found: ", pop[i])
                return pop[i]
        new_pop = []
        while len(new_pop) < pop_size:
            parent1 = _selection(pop, scores)
            parent2 = _selection(pop, scores)
            # keep parents in the population
            new_pop.extend([parent1, parent2])
            # add new children
            child1 = _crossover(parent1, parent2)
            child2 = _crossover(parent1, parent2)
            child1 = _mutation(child1, mutation_rate)
            child2 = _mutation(child1, mutation_rate)
            new_pop.extend([child1, child2])
        while len(new_pop) > pop_size:
            new_pop.pop()
        pop = new_pop
    return -1






if __name__ == '__main__':
    #b = [(7, 7), (7, 9), (2, 3), (9, 9), (4, 9)]
    #print(simultaneous_incongruence(b))
    #print(genetic_algorithm(100, 100, b, 0.1))

   test(input())
